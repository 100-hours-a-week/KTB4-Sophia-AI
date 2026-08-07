"""
마스터 DB의 poster_path를 TMDB에서 한 번만 채우는 스크립트.

- 각 영화의 TMDB id로 /movie/{id} 를 호출해 poster_path를 받아 DB에 저장.
- poster_path가 아직 비어있는(NULL) 영화만 처리 → 여러 번 돌려도 안전.
- 이거 한 번 돌려두면, 이후 챗봇은 실시간 API 없이 DB에서 포스터를 바로 씀.

사용법: python fill_posters.py
필요: pip install requests python-dotenv
"""
import requests
import time
import sqlite3
from config import TMDB_TOKEN

DB_FILE = "master.db"

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

# poster_path가 아직 없는 영화만 골라오기
rows = cur.execute(
    "SELECT id, title_kor FROM movies WHERE poster_path IS NULL"
).fetchall()
print(f"채울 영화: {len(rows)}개")

filled, failed = 0, 0
for movie_id, title in rows:
    try:
        r = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}",
            params={"language": "ko-KR"},                       # api_key 뺌
            headers={"Authorization": f"Bearer {TMDB_TOKEN}"},  # 헤더로 인증
            timeout=10,
        )
        print("상태코드:", r.status_code)
        print("응답:", r.text[:200])
        path = r.json().get("poster_path")     # 예: "/abc.jpg"
        cur.execute(
            "UPDATE movies SET poster_path = ? WHERE id = ?",
            (path, movie_id),
        )
        filled += 1
        print(f"   O {title}: {path}")
    except Exception as e:
        failed += 1
        print(f"  X {title}: 실패 - {e}")
    time.sleep(0.05)   # 연속 호출 살짝 텀 (rate limit 예방)

conn.commit()
conn.close()
print(f"\n완료! 성공 {filled}개, 실패 {failed}개")
