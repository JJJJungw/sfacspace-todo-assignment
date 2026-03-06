from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import SessionLocal
from .. import models, schemas

router = APIRouter(prefix="/todos", tags=["todos"])

#db세션 관리용 - ex) @trainsactional 같은 역할
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. 할 일 생성 (POST /todos)
@router.post("/", response_model=schemas.TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    db_todo = models.Todo(title=todo.title, description=todo.description, is_done=todo.is_done)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# 2. 할 일 목록 조회 (GET /todos)
@router.get("/", response_model=List[schemas.TodoResponse])
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):  
    # 1. 쿼리 객체 생성 (전략 수립)
    statement = select(models.Todo).offset(skip).limit(limit)
    
    # 2. 쿼리 실행 (DB에 전송)
    result = db.execute(statement)
    
    # 3. 결과 가공 (객체 추출)
    todos = result.scalars().all()
    
    # 4. 반환 (DTO 변환)
    return todos

from fastapi import HTTPException, status

# 3. 할 일 단건 상세 조회 (GET /todos/{todo_id})
@router.get("/{todo_id}", response_model=schemas.TodoResponse)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    # [1단계] DB에서 PK(Primary Key)로 조회 (JPA의 em.find() 역할)
    # 2.0 방식에서도 단건 PK 조회는 db.get()이 가장 빠르고 표준.
    db_todo = db.get(models.Todo, todo_id)
    
    # [2단계] 결과 검증 
    if db_todo is None:
        # 데이터가 없으면 404 에러를 발생
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"ID {todo_id}번에 해당하는 todo를 찾을 수 없습니다."
        )
    return db_todo

# 4. 할 일 수정 (PUT /todos/{todo_id})
@router.put("/{todo_id}", response_model=schemas.TodoResponse)
def update_todo(todo_id: int, todo_update: schemas.TodoUpdate, db: Session = Depends(get_db)):
    # [1단계] 수정할 데이터 조회 (findById)
    db_todo = db.get(models.Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="수정할 todo를 찾을 수 없습니다.")

    # [2단계] 데이터 업데이트 (Pydantic의 편리한 기능 사용)
    # todo_update.model_dump(exclude_unset=True)는 
    # 클라이언트가 보낸 값들만 추출합니다. (보내지 않은 필드는 무시)
    update_data = todo_update.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_todo, key, value) # 객체의 필드 값을 동적으로 변경

    # [3단계] 반영 및 커밋
    db.add(db_todo) # 생략 가능하지만 명시적으로 추가
    db.commit()     # JPA의 트랜잭션 종료 시점과 동일
    db.refresh(db_todo)
    return db_todo


# 5. 할 일 삭제 (DELETE /todos/{todo_id})
@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    # [1단계] 삭제할 데이터 조회
    db_todo = db.get(models.Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="삭제할 todo를 찾을 수 없습니다.")

    # [2단계] 삭제 처리
    db.delete(db_todo)
    db.commit()
    return None

