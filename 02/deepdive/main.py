from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 서버에 접근 가능한 항목의 리스트
origins = [
    # 지금 테스트 중인 브라우저 주소(클라이언트)
    "http://127.0.0.1:5500", 
    "http://localhost:5500",
]

# 미들웨어(중간 관리자)를 추가해 CORS 규칙 적용
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     # 허용할 출처
    allow_credentials=True,    # 쿠키나 인증 정보 허용
    allow_methods=["*"],       # GET, POST 등 모든 메서드 허용
    allow_headers=["*"],       # 모든 헤더 허용
)

# 모델 추론 요청
@app.post("/predict")
def predict_model(data: dict):
    return {"result": "정상적으로 추론되었습니다!"}