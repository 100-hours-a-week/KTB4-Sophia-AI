from fastapi import FastAPI
from rag_langgraph import answer
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from rag_langgraph import answer_stream

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