# 명령 넣는 파일
# 성공/에러 메시지
import aiosqlite
import sqlite3
import ollama
from models import PostUpdate

# Ollama API로 본문 내용 요약
async def generate_summary(content: str):
    response = await ollama.chat(model='gemma4', messages=[
        {'role': 'system', 'content': "너는 요약 전문 AI야."},
        {'role': 'user', 'content': f"다음 글 내용을 50자 이내로 요약해줘:\n\n{content}"},
    ])
    return response['message']['content']

async def get_posts_from_db_with_nickname(nickname: str = None):
    async with aiosqlite.connect("web_project.db") as conn:
        # 데이터를 이름으로 꺼내기 위해서 하는 설정
        conn.row_factory = sqlite3.Row

        # nickname이 없으면 전체 글을 보여줌
        if nickname is None:
            async with conn.execute("SELECT * FROM posts") as cursor:
                rows = await cursor.fetchall()
        else: # posts에서 닉네임이 ?인 데이터만 고르기
            # ,를 찍어서 값이 하나인 튜플임을 명시
            async with conn.execute("SELECT * FROM posts WHERE nickname = ?", (nickname,)) as cursor:
                # rows 변수에 방금 수행한 결과를 모두 담기
                rows = await cursor.fetchall()
        return [dict(row) for row in rows]

async def get_posts_from_db_with_id(post_id: int):
    async with aiosqlite.connect("web_project.db") as conn:
        conn.row_factory = sqlite3.Row

        # 가독성을 위해 posts라고 하기
        async with conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)) as cursor:
            rows = await cursor.fetchall()

        # DB에서 가져온 데이터를 딕셔너리 리스트로 변환
        return [dict(row) for row in rows]
    
async def update_post_in_db(post_id: int, updated_post: PostUpdate):
    async with aiosqlite.connect("web_project.db") as conn:
        conn.row_factory = sqlite3.Row

        async with conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)) as cursor:
            row = await cursor.fetchone()

        if row is None:
            # 에러 여부를 판단할 수 있는 메시지만 보여줌
            return {"status": "not_found"}
        
        if row['password'] != updated_post.password:
            return {"status": "wrong_password"}

        summary = await generate_summary(updated_post.content)
        await conn.execute("UPDATE posts SET title = ?, content = ?, summary = ? WHERE id = ?", (updated_post.title, updated_post.content, summary, post_id))
        await conn.commit()

    # 수정 성공 메시지 출력
    return {"status": "success"}

# delete API
async def delete_post_in_db(post_id: int, password: int):
    async with aiosqlite.connect("web_project.db") as conn:
        conn.row_factory = sqlite3.Row

        async with conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)) as cursor:
            row = await cursor.fetchone()

        if row is None:
            return {"status": "not_found"}
        
        if row['password'] != password:
            return {"status": "wrong_password"}

    return {"status": "success"}