from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from config import CHROMA_DIR, GEMINI_API_KEY
from langchain_chroma import Chroma

# 바닐라 rag.py를 LangChain으로 마이그레이션한 버전
# 같은 ChromaDB를 불러와 검색 + 답변 생성을 LangChain 방식(리트리버 + LCEL 체인)으로 처리함
# app_langchain.py가 answer 함수를 import해서 사용할 것임

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=GEMINI_API_KEY,
)

# 벡터스토어 불러오기
# 저장된 movies 컬렉션 불러오기
vectorstore = Chroma(
    collection_name="movies",
    embedding_function=embeddings,
    persist_directory=CHROMA_DIR,
)

print(f"VectorStore 준비 완료: {type(vectorstore).__name__}")

# 리트리버 만들기
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5},
)

print(f"Retriever 객체: {type(retriever).__name__}")

# 검색된 문서들을 참고 자료 텍스트로 정리
def format_docs(docs):
    return "\n\n".join(
        f'[{d.metadata["title_kor"]} ({d.metadata["year"]}) | 평점 {d.metadata["rating"]} | {d.metadata["genres"]}]\n'
        f'{d.page_content}\n출처: {d.metadata["source_url"]}'
        for d in docs
    )

# 프롬프트 템플릿
SYSTEM_PROMPT = """
너는 영화를 추천하고 관련 질문에 답하는 챗봇이야.
아래 '참고 자료'는 실제 데이터베이스에서 검색된 진짜 영화 정보야. 신뢰하고 활용해.
추천은 참고 자료에 있는 작품 중에서만 골라. 자료에 없는 작품을 지어내지 마.
자료에 상세 줄거리가 없으면 있는 정보로 최대한 답하고, 사용자가 명시적으로 결말/스포일러를 요청한 경우에만 포함해서 알려줘.
답변은 한국어로 하고, 이모지는 과하지 않게 사용해."""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT + "\n\n=== 참고 자료 ===\n{context}"),
    ("human", "{question}")
])

# 모델 + 파서
model = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    google_api_key=GEMINI_API_KEY,
)
parser = StrOutputParser()

# 체인 구성 (LCEL)
chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | model
    | parser
)

# answer 함수
def answer(query):
    return chain.invoke(query)

# 테스트
# print(answer("우주를 배경으로 하는 SF 영화 추천해줘"))