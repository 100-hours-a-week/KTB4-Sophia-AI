import json, time, os
import requests
from config import DATA_DIR

WIKI_API = "https://en.wikipedia.org/w/api.php"

# 위키백과에서 줄거리 찾아오기
def get_plot(title_en, year=None):
    # 영어 원제목이 비어있으면 빈칸
    if not title_en:
        return ""
    
    # 시도할 제목 후보
    # 먼저, 정확한 제목만
    candidates = []
    if year:
        candidates.append(f"{title_en} ({year} film)")
    candidates.append(f"{title_en} (film)")
    candidates.append(title_en)

    # 프로젝트 이름/버전/설명 없으면 막힘..!
    headers = {"User-Agent": "movie-rag-project/1.0 (student project)"}

    for name in candidates:
        params = {
            "action": "query", "format": "json", "titles": name,
            "prop": "extracts", "explaintext": True, "redirects": 1,
        }

        try:
            for attempt in range(3):
                r = requests.get(WIKI_API, params=params, headers=headers, timeout=15)
                if r.status_code == 429:
                    time.sleep(5)
                    continue
                break
            # r을 딕셔너리로 바꿔서 담기
            data = r.json()
            # query에 들어있는 pages 항목
            pages = data["query"]["pages"]
            # pages 생김새
            # pages = {"27205": {"title": "Inception", "extract": "본문..."}}
            # .values: 숫자 말고 값들만 뽑아
            # iter(~): 하나씩 꺼낼 준비
            # next(~): 첫번째 문서 하나 꺼내줌
            page = next(iter(pages.values()))
            # 꺼낸 문서에서 extract(본문 전체 텍스트) 꺼내서 text에 담기
            text = page.get("extract", "")
            if not text:
                continue

            for header in ["== Plot ==", "== Plot summary ==", "== Synopsis =="]:
                if header in text:
                    # == Plot == 뒤부터 끝까지 자르기
                    after = text.split(header, 1)[1]
                    # Plot 섹션만 떼어내기
                    plot = after.split("\n== ", 1)[0]
                    # 앞뒤 공백 정리해서 돌려주기
                    return plot.strip()

        except Exception:
            continue
    return ""

records = []
with open(os.path.join(DATA_DIR, "movies.jsonl"), encoding="utf-8") as f:
    for line in f:
        records.append(json.loads(line))

before = sum(1 for r in records if r["plot"])

# get_plot 반복하기
# records 하나씩 돌면서 번호(i), 영화(r) 받기
for i, r in enumerate(records):
    # 영어 제목이 있다면
    if r["title_en"] and not r["plot"]:
        # 영어 제목으로 위키에서 줄거리를 찾아 plot에 저장
        r["plot"] = get_plot(r["title_en"], r.get("year"))
    # 10개마다 상태 보여주기
    if i % 10 == 0:
        print(f"진행 중... {i}/{len(records)}")
    time.sleep(0.5)
    
# 채워진 영화 세기
after = sum(1 for r in records if r["plot"])

print(f"작업 전 채워져 있던 영화: {before}개")
print(f"이번에 새로 채운 영화: {after - before}개")
print(f"전테 채워짐: {after}/{len(records)}")
print(f"아직 못 채운 영화: {len(records) - after}개")

with open(os.path.join(DATA_DIR, "movies.jsonl"), "w", encoding="utf-8") as f:
    for r in records:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("records 저장 완료")