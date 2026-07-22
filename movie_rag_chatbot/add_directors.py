# movies.jsonl 불러오기 (줄거리 이미 있는 상태)
# 각 영화마다 TMDB에서 감독 이름 가져오기
# r["director"] = 감독 이름  (필드 추가)
# 다시 저장하기 (줄거리랑 감독 둘 다 있는 상태)

import json, time, os
import requests
from config import DATA_DIR, TMDB_TOKEN

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

def get_director(m_id):
    data = tmdb_get(f"/movie/{m_id}/credits", {})
    directors = [c["name"] for c in data["crew"] if c["job"] == "Director"]
    return ", ".join(directors)

# 수집 루프
records = []
with open(os.path.join(DATA_DIR, "movies.jsonl"), encoding="utf-8") as f:
    for line in f:
        records.append(json.loads(line))

# get_director 반복하기
# records 하나씩 돌면서 번호(i), 영화(r) 받기
for i, r in enumerate(records):
    # id로 검색해서 감독 저장하기
    r["director"] = get_director(r["id"])
    # 10개마다 상태 보여주기
    if i % 10 == 0:
        print(f"진행 중... {i}/{len(records)}")
    time.sleep(0.2)
    
# 채워진 영화 세기
filled = sum(1 for r in records if r["director"])
print(f"감독 추가 완료: {filled}/{len(records)}")

with open(os.path.join(DATA_DIR, "movies.jsonl"), "w", encoding="utf-8") as f:
    for r in records:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("감독 이름 저장 완료")