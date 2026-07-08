import os
import json
import chromadb
from chromadb.utils import embedding_functions
from config import DATA_DIR, CHROMA_DIR, GOOGLE_API_KEY

# 텍스트 자르는 함수
def chunk_text(text, size=500, overlap=100):
    chunks = []
    text = (text or "").strip()
    if not text:
        return []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start += size - overlap
    return chunks

# records 돌면서 조각내고 꼬리표 만들기
docs = []
metadatas = []
ids = []

# 나중에 재실행했을 때를 대비해서 records는 비우고
# 저장한 내용 불러오기
records = []
with open(os.path.join(DATA_DIR, "movies.jsonl"), "r", encoding="utf-8") as f:
    for line in f:
        records.append(json.loads(line))
print("불러온 영화 수: ", len(records))

for r in records:
    base_meta = {
        "id": r["id"],
        "title_kor": r["title_kor"],
        "title_en": r["title_en"],
        "year": r["year"],
        "genres": ", ".join(r["genres"]),
        "keywords": ", ".join(r["keywords"]),
        "casts": ", ".join(r["casts"]),
        "rating": float(r["rating"]),
        "source_url": r["source_url"],
    }

    # enumerate: 리스트 돌 때 몇번째 + 항목 주는 도구
    for i, c in enumerate(chunk_text(r["overview"])):
        docs.append(c)
        # **base_meta를 해야 내용이 펼쳐져서 들어감
        metadatas.append({**base_meta, "spoiler": False, "section": "overview"})
        ids.append(f"{r['id']}_overview_{i}")

    for i, c in enumerate(chunk_text(r["plot"])):
        docs.append(c)
        # **base_meta를 해야 내용이 펼쳐져서 들어감
        metadatas.append({**base_meta, "spoiler": True, "section": "plot"})
        ids.append(f"{r['id']}_plot_{i}")

print("총 청크: ", len(docs))


# k: key, v: value
# m: 딕셔너리 하나, m.items: 딕셔너리 내부의 키,값 한 쌍씩 순회
def clean_meta(m):
    return {k: ("N/A" if (v is None or v == "") else v) for k, v in m.items()}

metadatas = [clean_meta(m) for m in metadatas]

ef = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
    api_key=GOOGLE_API_KEY,
    model_name="models/text-embedding-004")
client = chromadb.PersistentClient(path=CHROMA_DIR)

# 전에 만들어둔 collection이 있다면 삭제하고 다시 만들기 (오류 방지)
COLL = "movies"
try:
    client.delete_collection(COLL)
except Exception:
    pass
collection = client.create_collection(COLL, embedding_function=ef)

B = 100
for i in range(0, len(docs), B):
    collection.add(
        documents=docs[i:i + B],
        metadatas=metadatas[i:i + B],
        ids=ids[i:i + B],
    )

print("저장 개수: ", collection.count())
print("메타 확인: ", collection.get(limit=1, include=["metadatas"])["metadatas"])