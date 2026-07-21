from fastapi import FastAPI
from rag_langgraph import answer
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

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