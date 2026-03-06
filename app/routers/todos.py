from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession # [변경] 비동기 세션 타입
from typing import List

from ..database import get_db # database.py에서 만든 비동기 get_db 사용
from .. import models, schemas

router = APIRouter(prefix="/todos", tags=["todos"])

# 1. 할 일 생성 (POST /todos)
@router.post("/", response_model=schemas.TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: schemas.TodoCreate, db: AsyncSession = Depends(get_db)):
    # Pydantic V2의 model_dump() 사용
    db_todo = models.Todo(**todo.model_dump()) 
    db.add(db_todo)
    await db.commit()   # await 추가
    await db.refresh(db_todo) # await 추가
    return db_todo

# 2. 할 일 목록 조회 (GET /todos)
@router.get("/", response_model=List[schemas.TodoResponse])
async def read_todos(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):  
    statement = select(models.Todo).offset(skip).limit(limit)
    
    # await db.execute() 사용
    result = await db.execute(statement)
    
    todos = result.scalars().all()
    return todos

# 3. 할 일 단건 상세 조회 (GET /todos/{todo_id})
@router.get("/{todo_id}", response_model=schemas.TodoResponse)
async def read_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    # [변경] await db.get() 사용
    db_todo = await db.get(models.Todo, todo_id)
    
    if db_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"ID {todo_id}번에 해당하는 todo를 찾을 수 없습니다."
        )
    return db_todo

# 4. 할 일 수정 (PUT /todos/{todo_id})
@router.put("/{todo_id}", response_model=schemas.TodoResponse)
async def update_todo(todo_id: int, todo_update: schemas.TodoUpdate, db: AsyncSession = Depends(get_db)):
    # [변경] await db.get()
    db_todo = await db.get(models.Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="수정할 todo를 찾을 수 없습니다.")

    update_data = todo_update.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_todo, key, value)

    # db.add(db_todo) # SQLAlchemy에서는 영속성 컨텍스트 덕분에 수정 시 생략 가능
    await db.commit()   # await 추가
    await db.refresh(db_todo)
    return db_todo

# 5. 할 일 삭제 (DELETE /todos/{todo_id})
@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    # [변경] await db.get()
    db_todo = await db.get(models.Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="삭제할 todo를 찾을 수 없습니다.")

    await db.delete(db_todo) # delete 자체는 await가 필요없지만 commit은 필요
    await db.commit()        # await 추가