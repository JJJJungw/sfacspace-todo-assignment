from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..database import get_db
from .. import schemas, crud

router = APIRouter(prefix="/todos", tags=["todos"])

# 1. 할 일 생성 (POST /todos)
@router.post("/", response_model=schemas.TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: schemas.TodoCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_todo(db=db, todo=todo)

# 2. 할 일 목록 조회 (GET /todos)
@router.get("/", response_model=List[schemas.TodoResponse])
async def read_todos(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):  
    return await crud.get_todos(db=db, skip=skip, limit=limit)

# 3. 할 일 단건 상세 조회 (GET /todos/{todo_id})
@router.get("/{todo_id}", response_model=schemas.TodoResponse)
async def read_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    db_todo = await crud.get_todo(db=db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"ID {todo_id}번에 해당하는 todo를 찾을 수 없습니다."
        )
    return db_todo

# 4. 할 일 수정 (PUT /todos/{todo_id})
@router.put("/{todo_id}", response_model=schemas.TodoResponse)
async def update_todo(todo_id: int, todo_update: schemas.TodoUpdate, db: AsyncSession = Depends(get_db)):
    db_todo = await crud.update_todo(db=db, todo_id=todo_id, todo_update=todo_update)
    if db_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"ID {todo_id}번에 해당하는 todo를 찾을 수 없습니다."
        )
    return db_todo

# 5. 할 일 삭제 (DELETE /todos/{todo_id})
@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    result = await crud.delete_todo(db=db, todo_id=todo_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"ID {todo_id}번에 해당하는 todo를 찾을 수 없습니다."
        )
    return None
