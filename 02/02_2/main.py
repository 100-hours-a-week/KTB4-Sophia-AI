from fastapi import FastAPI
from routers import posts

app = FastAPI()

# posts db 관련 라우터 연결
app.include_router(posts.router, prefix="/posts")