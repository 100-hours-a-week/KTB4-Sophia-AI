import chromadb
from chromadb.utils import embedding_functions
import google.generativeai as genai
from config import CHROMA_DIR, GOOGLE_API_KEY

# rag.py
# 저장된 ChromaDB를 불러와 검색 + 답변 생성을 담당함
# app.py가 answer 함수를 import해서 사용할 예정

# ChromaDB 불러오기 + 클로드 클라이언트 준비
# all_titles_kor: 제목 인식 검색용 영화 제목 목록
# search(): 질문으로 관련 영화 조각 검색 (제목 인식 + 스포일러 필터)
# build_context(): 검색 결과를 클로드용 참고 자료 텍스트로 정리
# answer(): 참고 자료를 근거로 클로드가 답변 생성

ef = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
    api_key=GOOGLE_API_KEY,
    model_name="models/text-embedding-004")
client = chromadb.PersistentClient(path=CHROMA_DIR)

collection = client.get_collection("movies", embedding_function=ef)

# 한글 제목 다 모으기 (제목 검색을 위해서))
all_titles_kor = list({m["title_kor"] for m in collection.get(include=["metadatas"])["metadatas"] if m["title_kor"]})

def search(query, n_results=5, spoiler_free=True):

    mentioned = [t for t in all_titles_kor if t in query]
    if mentioned:
        where = {"title_kor": {"$in": mentioned}}
    else:
        where = {"spoiler": False} if spoiler_free else None

    results = collection.query(
          query_texts=[query],
          n_results=n_results,
          where=where,
    )
    return results

# 제미나이 클라이언트 불러오기
genai.configure(api_key=GOOGLE_API_KEY)
gemini_client = genai.GenerativeModel("gemini-1.5-flash")

def build_context(query, n_results=5, spoiler_free=True):
    result = search(query, n_results=n_results, spoiler_free=spoiler_free)
    docs = result["documents"][0]
    metas = result["metadatas"][0]
    if not docs:
        return ""
    blocks = []
    for doc, meta in zip(docs, metas):                                       # ← for문 복구
        blocks.append(
            f'[{meta["title_kor"]} ({meta["year"]}) | 평점 {meta["rating"]} | {meta["genres"]}]\n'
            f'{doc}\n출처: {meta["source_url"]}'
        )
    return "\n\n".join(blocks)

# 답변 생성하기
SYSTEM_PROMPT = """
너는 영화를 추천하고 관련 질문에 답하는 챗봇이야.
아래 '참고 자료'는 실제 데이터베이스에서 검색된 진짜 영화 정보야. 신뢰하고 활용해.
추천은 참고 자료에 있는 작품 중에서만 골라. 자료에 없는 작품을 지어내지 마.
자료에 상세 줄거리가 없으면 있는 정보로 최대한 답하고, 사용자가 명시적으로 결말/스포일러를 요청한 경우에만 포함해서 알려줘.
답변은 한국어로 하고, 이모지는 과하지 않게 사용해."""

def answer(query, spoiler_free=True):
    # R + A: 관련 자료 검색해서 참고 자료 텍스트 만들기
    context = build_context(query, spoiler_free=spoiler_free)
    # 참고 자료를 시스템 프롬프트에 끼워 넣기
    system = SYSTEM_PROMPT + "\n\n=== 참고 자료 ===\n" + (context or "관련 자료 없음")
    # G: 제미나이가 참고 자료를 근거로 답 생성
    response = gemini_client.generate_content(system + "\n\n" + query)
    return response.text