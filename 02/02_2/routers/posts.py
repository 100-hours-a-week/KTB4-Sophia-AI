from fastapi import APIRouter
from fastapi import HTTPException
from models import (PostCreate, PostUpdate)
from controllers import (generate_summary,
                         get_posts_from_db_with_nickname,
                         get_posts_from_db_with_id,
                         update_post_in_db,
                         delete_post_in_db)

# 라우터 객체 생성
router = APIRouter()

# @app 대신 @router
@router.post("", status_code=201)
async def create_post(post: PostCreate):
    summary = await generate_summary(post)

    # 어떤 데이터를 받았는지 웹에 확인 메시지
    # model_dump()는 데이터를 딕셔너리로 변환해서 모두 보여줌
    return {"message": "글이 성공적으로 전송되었습니다", "data": post.model_dump()}

# 요청을 받았을때 nickname이라는 id인지, 닉네임인지 헷갈리니까 /post로 설정
@router.get("", status_code=200)
# str = None: nickname을 입력하지 않아도 됨
async def read_post_by_nickname(nickname: str = None):
    # controllers.py에 있는 함수 불러옴
    rows = await get_posts_from_db_with_nickname(nickname)

    # 검색했는데 해당 닉네임으로 쓰인 글이 없을때
    if nickname and len(rows) == 0:
        raise HTTPException(status_code=404, detail="해당하는 닉네임의 글이 없습니다.")

    return rows

@router.get("/{post_id}", status_code=200)
async def read_post_by_id(post_id: int):
    rows = await get_posts_from_db_with_id(post_id)

    if post_id and len(rows) == 0:
        raise HTTPException(status_code=404, detail="해당하는 글이 없습니다.")

    return rows

@router.put("/{post_id}", status_code=201)
# 게시글 수정 API
async def correct_post(post_id: int, updated_post: PostUpdate):
    result = await update_post_in_db(post_id, updated_post)

    # status에 따라 응답
    if result["status"] == "not_found":
        raise HTTPException(status_code=404, detail="해당하는 글이 없습니다.")
        
    if result["status"] == "wrong_password":
        raise HTTPException(status_code=401, detail="비밀번호가 틀렸습니다.")

    # 수정 성공 메시지 출력
    return {"message": "글이 성공적으로 수정되었습니다."}
    
# delete API
@router.delete("/{post_id}", status_code=200)
async def delete_post(post_id: int, password: int):
    result = await delete_post_in_db(post_id, password)

    if result["status"] == "not_found":
        raise HTTPException(status_code=404, detail="해당하는 글이 없습니다.")
        
    if result["status"] == "wrong_password":
        raise HTTPException(status_code=401, detail="비밀번호가 틀렸습니다.")

    return {"message": "글이 성공적으로 삭제되었습니다."}