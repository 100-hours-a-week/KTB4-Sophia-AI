import json, csv
from collections import Counter

records = []
with open("data/movies.jsonl", encoding="utf-8") as f:
    for line in f:
        records.append(json.loads(line))

print("총 영화 수: ", len(records))

# 장르별 개수
counter = Counter()
for r in records:
    for g in r.get("genres", []):
        counter[g] += 1
print("\n=== 장르별 영화 수===")
for g, c in counter.most_common():
    print(f"{g}: {c}")

# 줄거리 채워진 개수
filled = sum(1 for r in records if r.get("plot"))
print(f"\n상세 줄거리 있는 영화: {filled}/Plen(records)")

# CSV로 저장
with open("movies_view_2.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["제목", "연도", "장르", "평점", "출연", "줄거리있음"])
    for r in records:
        w.writerow([
            r.get("title_kor", ""), r.get("year", ""),
            ", ".join(r.get("genres", [])), r.get("rating", ""),
            ", ".join(r.get("casts", [])), "O" if r.get("plot") else "X",
        ])
print("\nmovies_view_2.csv 저장 완료")

# 제목, 장르, 줄거리 여부만 CSV로 저장
with open("movies_title_genre_view_2.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["제목", "장르", "줄거리있음"])
    for r in records:
        w.writerow([
            r.get("title_kor", ""),
            ", ".join(r.get("genres", [])), "O" if r.get("plot") else "X",
        ])
print("\nmovies_title_genre_view_2.csv 저장 완료")