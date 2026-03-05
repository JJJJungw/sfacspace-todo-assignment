from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class TodoBase(BaseModel):
    # 필수 필드 (Request 시 반드시 포함되어야 함)
    title: str = Field(..., min_length=1, max_length=255, description="제목")
    # 선택 필드 (Request 시 없어도 에러 안 남)
    description: Optional[str] = Field(None, max_length=500, description="상세 설명")
    is_done: bool = Field(default=False, description="완료 여부")

class TodoCreate(TodoBase):
    pass

class TodoResponse(TodoBase):
    id: int = Field(..., description="할 일 ID")
    created_at: datetime = Field(..., description="생성 시간")
    model_config = ConfigDict(from_attributes=True)

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="제목")
    description: Optional[str] = Field(None, max_length=500, description="상세 설명")
    is_done: Optional[bool] = Field(None, description="완료 여부")
