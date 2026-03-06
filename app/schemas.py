from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
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
    
    # [핵심] SQLAlchemy 객체(ORM)를 Pydantic으로 자동 변환해주는 설정
    model_config = ConfigDict(from_attributes=True) 

class TodoUpdate(BaseModel):
    # 업데이트는 모든 필드가 선택적(Optional)이어야 함
    title: str | None = None
    description: str | None = None
    is_done: bool | None = None