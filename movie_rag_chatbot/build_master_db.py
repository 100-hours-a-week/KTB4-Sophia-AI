"""
jsonl(영화 데이터) → SQLite 마스터 DB 변환 스크립트

- 입력: movies.jsonl  (한 줄당 영화 하나, JSON 객체)
- 출력: master.db     (movies 테이블)
사용법: python build_master_db.py

* 줄거리(plot)는 스포일러라 벡터DB에서 검색용으로 쓰니까, 마스터 DB엔 안 넣음.
  마스터 DB는 '정형 정보(제목·평점·감독·출연 등)의 단일 진실 공급원' 역할.
"""

import json
import sqlite3

JSONL_FILE = "data/movies.jsonl"
DB_FILE = "master.db"         # 만들어질 마스터 DB 파일명

# 1. DB 연결
conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

# 2. 테이블 생성 (여러 번 돌려도 안전하게 DROP 후 재생성)
cur.execute("DROP TABLE IF EXISTS movies")
cur.execute("""
CREATE TABLE movies (
    id          INTEGER PRIMARY KEY,  -- TMDB movie id (벡터DB·TMDB와 연결하는 열쇠)
    title_kor   TEXT,   -- 한글 제목
    title_en    TEXT,   -- 영문 제목
    year        INTEGER,
    genres      TEXT,   -- "모험, 드라마, SF"
    rating      REAL,   -- 평점
    casts       TEXT,   -- "매튜 매커너히, 앤 해서웨이, ..."
    director    TEXT,   -- 감독
    overview    TEXT,   -- 한글 개요 (스포 없음)
    keywords    TEXT,   -- 키워드
    source_url  TEXT,   -- TMDB 페이지 주소
    poster_path TEXT    -- 포스터 경로 (지금은 비움, 나중에 TMDB에서 채움)
)
""")

# 3. jsonl 한 줄씩 읽어서 넣기
count = 0
with open(JSONL_FILE, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        m = json.loads(line)   # 한 줄 = 영화 하나
        cur.execute(
            """INSERT OR REPLACE INTO movies
               (id, title_kor, title_en, year, genres, rating, casts,
                director, overview, keywords, source_url, poster_path)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                m.get("id"),
                m.get("title_kor"),
                m.get("title_en"),
                m.get("year"),
                ", ".join(m.get("genres", [])),    # 리스트 → 문자열
                m.get("rating"),
                ", ".join(m.get("casts", [])),
                m.get("director"),
                m.get("overview"),
                ", ".join(m.get("keywords", [])),
                m.get("source_url"),
                None,   # poster_path: 나중에 TMDB에서 채워 넣을 자리
            ),
        )
        count += 1

# 4. 저장하고 마무리
conn.commit()
print(f"완료! {count}개 영화를 master.db에 저장했어요.")

# 5. 확인용 — 인셉션 조회
conn.row_factory = sqlite3.Row
row = conn.execute(
    "SELECT id, title_kor, rating, director FROM movies WHERE title_kor = ?",
    ("인셉션",),
).fetchone()
if row:
    print("샘플 조회:", dict(row))

conn.close()