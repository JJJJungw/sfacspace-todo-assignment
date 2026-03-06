from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(None, max_length=500) # Optional 대신 | None 사용
    is_done: bool = False

class TodoCreate(TodoBase):
    pass

class TodoResponse(TodoBase):
    id: int
    created_at: datetime
    
    # [핵심] FastAPI에서 SQLAlchemy ORM 객체를 Pydantic 모델로 변환할 때 필요한 설정
    model_config = ConfigDict(from_attributes=True) 

class TodoUpdate(BaseModel):
    # 업데이트는 모든 필드가 선택적(Optional)이어야 함
    title: str | None = None
    description: str | None = None
    is_done: bool | None = None