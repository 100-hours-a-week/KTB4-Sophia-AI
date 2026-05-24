from pydantic import BaseModel
from fastapi import FastAPI
from fastapi import HTTPException
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
@app.post("/posts", status_code=201)
# post에 PostCreate 클래스를 저장
def create_post(post: PostCreate):
    # Ollama로 요약본 만들기
    summary = generate_summary(post.content)
    # DB 연결
    # conn: DB의 문을 여는 행위
    conn = sqlite3.connect("web_project.db")
    # cursor: 동작 수행
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

@app.get("/posts", status_code=200)
# str = None: nickname을 입력하지 않아도 됨
def read_post_by_nickname(nickname: str = None):
    # DB 연결
    conn = sqlite3.connect("web_project.db")
    # 데이터를 이름으로 꺼내기 위해서 하는 설정
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # nickname이 없으면 전체 글을 보여줌
    if nickname is None:
        cursor.execute("SELECT * FROM posts")
        rows = cursor.fetchall()
    else: # posts에서 닉네임이 ?인 데이터만 고르기
        # ,를 찍어서 값이 하나인 튜플임을 명시
        cursor.execute("SELECT * FROM posts WHERE nickname = ?", (nickname,))
        # rows 변수에 방금 수행한 결과를 모두 담기
        rows = cursor.fetchall()

        # 검색했는데 해당 닉네임으로 쓰인 글이 없을때
        if len(rows) == 0:
            conn.close()
            raise HTTPException(status_code=404, detail="해당하는 닉네임의 글이 없습니다.")
    
    # DB와의 연결 끊기
    conn.close()

    # DB에서 가져온 데이터를 딕셔너리 리스트로 변환
    return [dict(row) for row in rows]

@app.get("/posts/{post_id}", status_code=200)
def read_post_by_id(post_id: int):
    conn = sqlite3.connect("web_project.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 가독성을 위해 posts라고 하기
    cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    rows = cursor.fetchall()

    if len(rows) == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="해당하는 글이 없습니다.")
        
    # DB와의 연결 끊기
    conn.close()

    # DB에서 가져온 데이터를 딕셔너리 리스트로 변환
    return [dict(row) for row in rows]

# 수정 클래스: 게시글 수정할 때는 닉네임 필요 없어서 새로 만들기
class PostUpdate(BaseModel):
    title: str
    content: str
    password: int

# 게시글 수정 API
@app.put("/posts/{post_id}", status_code=201)
def correct_post(post_id: int, updated_post: PostUpdate):
    conn = sqlite3.connect("web_project.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    rows = cursor.fetchall()

    if len(rows) == 0:
        conn.close()
        # 아이디가 존재하지 않을때 출력되는 메시지
        raise HTTPException(status_code=404, detail="해당하는 글이 없습니다.")
    else:
        cursor.execute("SELECT * FROM posts WHERE password = ?", (updated_post.password,))
        rows = cursor.fetchall()

        if len(rows) == 0:
            conn.close()
            # 비밀번호가 틀렸을때 출력되는 메시지
            raise HTTPException(status_code=401, detail="비밀번호가 틀렸습니다.")
        else:
            summary = generate_summary(updated_post.content)
            cursor.execute("UPDATE posts SET title = ?, content = ?, summary = ? WHERE id = ?", (updated_post.title, updated_post.content, summary, post_id))
            
            conn.commit()
            conn.close()

    # 수정 성공 메시지 출력
    return {"message": "글이 성공적으로 수정되었습니다."}

# delete API
@app.delete("/posts/{post_id}", status_code=200)
def delete_post(post_id: int, password: int):
    conn = sqlite3.connect("web_project.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    rows = cursor.fetchall()

    if len(rows) == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="해당하는 글이 없습니다.")
    else:
        cursor.execute("SELECT * FROM posts WHERE password = ?", (password,))
        rows = cursor.fetchall()

        if len(rows) == 0:
            conn.close()
            raise HTTPException(status_code=401, detail="비밀번호가 틀렸습니다.")
        else:
            cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
            conn.commit()
            conn.close()

    return {"message": "글이 성공적으로 삭제되었습니다."}