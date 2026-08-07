from fastapi import FastAPI
from rag_langgraph import answer
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from rag_langgraph import answer_stream
from fastapi.responses import FileResponse
import os, requests
from config import TMDB_TOKEN

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

# 요청 형식 정하기
# 요청에는 문자열 형식의 질문이 들어있다
# question: 이후에 질문 작성하기
class ChatRequest(BaseModel): question: str

# 엔드포인트 만들기
# /chat이 오면 answer 부르기
@app.post("/chat")
def chat(req: ChatRequest):
    result = answer(req.question)
    return {"answer": result}

@app.post("/chat/stream")
def chat_stream(req: ChatRequest):
    # answer_stream이 yield하는 조각들을 오는대로 브라우저로 내보냄
    # 조각을 계속 흘려보내게 함 (위의 기존 /chat과는 다름)
    return StreamingResponse(
        answer_stream(req.question),
        # 글자 조각을 보내준다고 알려줌
        media_type="text/plain",
    )

@app.get("/")
def home():
    return FileResponse("index.html")

TMDB_TOKEN = os.getenv("TMDB_TOKEN")

@app.get("/poster")
def poster(title: str):
    r = requests.get(
        "https://api.themoviedb.org/3/search/movie",
        params={"query": title, "language": "ko-KR"},
        headers={"Authorization": f"Bearer {TMDB_TOKEN}"},   # 헤더로 인증
    )
    results = r.json().get("results", [])
    path = results[0].get("poster_path") if results else None
    return {"url": f"https://image.tmdb.org/t/p/w500{path}" if path else None}