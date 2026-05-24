# PostUpdate 같은거 넣는 파일
from pydantic import BaseModel

# 글을 생성할 때 필요한 데이터
class PostCreate(BaseModel):
    title: str
    content: str
    nickname: str
    password: int

class PostUpdate(BaseModel):
    title: str
    content: str
    password: int