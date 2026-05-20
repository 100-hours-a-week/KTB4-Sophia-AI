from pydantic import BaseModel
from fastapi import FastAPI
import ollama
import sqlite3

app = FastAPI()

# 글을 생성할 때 필요한 데이터
class PostCreate(BaseModel):
    title: str
    content: str
    nickname: str
    password: int

# Ollama API로 본문 내용 요약
def generate_summary(content: str):
    response = ollama.chat(model='gemma4', messages=[
        {'role': 'system', 'content': "너는 요약 전문 AI야."},
        {'role': 'user', 'content': f"다음 글 내용을 50자 이내로 요약해줘:\n\n{content}"},
    ])
    return response['message']['content']

# 글 작성 API
# HTTP 메서드의 POST의 endpoint /posts
@app.post("/posts")
# post에 PostCreate 클래스를 저장
def create_post(post: PostCreate):
    # Ollama로 요약본 만들기
    summary = generate_summary(post.content)

    # DB 연결
    conn = sqlite3.connect("web_project.db")
    cursor = conn.cursor()

    # DB에 저장 (post 변수에서 데이터 꺼내서 SQL에 넣기)
    cursor.execute("""
        INSERT INTO posts (title, content, nickname, password, summary)
        VALUES (?, ?, ?, ?, ?)
    """, (post.title, post.content, post.nickname, post.password, summary))
    
    conn.commit()
    conn.close()

    # 어떤 데이터를 받았는지 웹에 확인 메시지
    # model_dump()는 데이터를 딕셔너리로 변환해서 모두 보여줌
    return {"message": "글이 성공적으로 전송되었습니다", "data": post.model_dump()}

@app.get("/posts")
# str = None: nickname을 입력하지 않아도 됨
def read_post_by_nickname(nickname: str = None):
    # nickname이 없으면 전체 글을 보여줌
    if nickname is None:
        return posts
    # 검색 결과 담는 리스트
    result = []
    # posts 안의 각각의 글인 p
    for p in posts:
        # p라는 글의 nickname이 내가 찾는 nickname이라면
        if p.nickname == nickname:
            # result 리스트에 글을 추가
            result.append(p)
    return result

@app.get("/posts/{post_id}")
def read_post_by_id(post_id: int):
    # 가독성을 위해 posts라고 하기
    for post in posts:
        if post.id == post_id:
            # 파이썬의 성질: return 실행하면 함수 종료
            return post
    return {"message": "해당하는 글이 없습니다."}