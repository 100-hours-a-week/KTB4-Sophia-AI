import os
import json
import time
import requests
from config import DATA_DIR, TMDB_TOKEN

# 수집 설정
LANG = "ko-KR"              # 한국어 제목/줄거리 우선
PAGES_PER_QUERY = 25         # 쿼리당 페이지 수
MIN_VOTES = 100             # 평점 참여수가 너무 적은 작품은 제외
USE_WIKIPEDIA = True        # 위키백과 상세 줄거리 보강

# 장르 ID (TMBD)
MOVIE_GENRES = "" # 빈 값 = 전체 장르

# tmdb_get, discover_ovie_ids, fetch_record 함수
# 데이터 수집 실행 (records에 저장)
# get_plot 함수 + 위키백과 줄거리 보강 실행
# movies.jsonl을 data에 저장

# 요청 보내는 함수
def tmdb_get(path, params):
    # BASE + path 합치기
    url = "https://api.themoviedb.org/3" + path
    # 토큰 헤더 + params 요청 보내기
    HEADERS = {"Authorization": f"Bearer {TMDB_TOKEN}", "accept": "application/json"}
    r = requests.get(url, headers=HEADERS, params=params)
    # 에러 확인하기
    r.raise_for_status()
    # 응답으로 온 JSON 글자를 파이썬 딕셔너리로 변환하기
    return r.json()

# 작품 ID 목록 모으는 함수
def discover_movie_ids(genres):
    # 모은 ID를 담을 빈 리스트
    ids = []
    # 페이지를 1부터 마지막 페이지까지 반복
    for p in range(1, PAGES_PER_QUERY + 1):
        # 각 페이지마다 params 딕셔너리 만들기
        params = {
            "sort_by": "vote_count.desc",
            "vote_count.gte": MIN_VOTES,
            "language": LANG,
            "page": p,
        }
        # 장르 필터: 장르가 있을 때만 추가하도록
        if genres:
            params["with_genres"] = genres
        # tmdb_get 불러오기
        data = tmdb_get(f"/discover/movie", params)
        # 불러온 결과에서 ID만 뽑아 리스트에 추가하기
        ids += [item["id"] for item in data.get("results", [])]
        # 차단을 피하기 위해 페이지마다 잠깐 쉬어주기
        time.sleep(0.2)
    # 반복 종료 후 딕셔너리로 만들어 중복 제거한 후 다시 리스트로 반환
    return list(dict.fromkeys(ids))

def fetch_record(m_id):
    # 상세 정보 받아오기
    d_ko = tmdb_get(f"/movie/{m_id}", params={"language": "ko-KR", "append_to_response": "keywords,credits"})
    d_en = tmdb_get(f"/movie/{m_id}", params={"language": "en-US"})
    # 필드 꺼내기: 제목, 영어 원제, 연도, 소개, 장르, 키워드, 출연, 평점
    title_kor = d_ko.get("title")
    title_en = d_en.get("title")
    date = d_ko.get("release_date")
    year = int(date[:4]) if date else 0
    overview = d_ko.get("overview") or d_en.get("overview") or ""
    genres = [g["name"] for g in d_ko.get("genres", [])]
    keywords = [k["name"] for k in d_ko.get("keywords", {}).get("keywords", [])]
    casts = [c["name"] for c in d_ko.get("credits", {}).get("cast", [])[:5]]
    rating = d_ko.get("vote_average", 0)
  
    # 딕셔너리로 묶어서 return
    return {
        "id": m_id,
        "title_kor": title_kor,
        "title_en": title_en,
        "year": year,
        "overview": overview,
        "genres": genres,
        "keywords": keywords,
        "casts": casts,
        "rating": rating,
        "type": "movie",
        "plot": "",
        "source_url": f"https://www.themoviedb.org/movie/{m_id}"
    }

# 수집 루프
records = []
# 영화 id 목록 받기
ids = discover_movie_ids(MOVIE_GENRES)
for i, m_id in enumerate(ids):
    try:
        # fetch_record 불러서 records에 추가
        records.append(fetch_record(m_id))
    except Exception as e:
        # 실패한 건 건너뛰고 알려주기
        print("skip", m_id, e)
    if i % 10 == 0:
        print(f"진행 중... {i}/{len(ids)}")
    time.sleep(0.2)
print(records[0])
print("총 영화 수: ", len(records), "개")

WIKI_API = "https://en.wikipedia.org/w/api.php"

# 위키백과에서 줄거리 찾아오기
def get_plot(title_en):
    # 영어 원제목이 비어있으면 빈칸
    if not title_en:
        return ""

    # 문서 본문 요청
    params = {
        "action": "query",
        "format": "json",
        "titles": title_en,
        "prop": "extracts",
        "explaintext": True,
        "redirects": 1,
    }
    headers = {"User-Agent": "movie-rag-project/1.0 (student project)"}
    try:
        for attempt in range(3):
            r = requests.get(WIKI_API, params=params, headers=headers, timeout=15)
            if r.status_code == 429:
                time.sleep(5)
                continue
            break
        data = r.json()
        pages = data["query"]["pages"]
        page = next(iter(pages.values()))
        text = page.get("extract", "")
        if not text:
            return ""

        for header in ["== Plot ==", "== Plot summary ==", "== Synopsis =="]:
            if header in text:
                # == Plot == 뒤부터 끝까지 자르기
                after = text.split(header, 1)[1]
                # Plot 섹션만 떼어내기
                plot = after.split("\n== ", 1)[0]
                # 앞뒤 공백 정리해서 돌려주기
                return plot.strip()
        return ""
    except Exception:
        return ""
    
# get_plot 반복하기
# records 하나씩 돌면서 번호(i), 영화(r) 받기
for i, r in enumerate(records):
    # 영어 제목이 있다면
    if r["title_en"]:
        # 영어 제목으로 위키에서 줄거리를 찾아 plot에 저장
        r["plot"] = get_plot(r["title_en"])
    # 10개마다 상태 보여주기
    if i % 10 == 0:
        print(f"진행 중... {i}/{len(records)}")
    time.sleep(0.5)
    
# 채워진 영화 세기
filled = sum(1 for r in records if r["plot"])
print(f"줄거리 보강 완료: {filled}/{len(records)}")

with open(os.path.join(DATA_DIR, "movies.jsonl"), "w", encoding="utf-8") as f:
    for r in records:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("records 저장 완료")