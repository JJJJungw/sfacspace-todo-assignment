from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas

async def get_todos(db: AsyncSession, skip: int = 0, limit: int = 100):
    statement = select(models.Todo).offset(skip).limit(limit)
    result = await db.execute(statement)
    return result.scalars().all()

async def get_todo(db: AsyncSession, todo_id: int):
    return await db.get(models.Todo, todo_id)

async def create_todo(db: AsyncSession, todo: schemas.TodoCreate):
    db_todo = models.Todo(**todo.model_dump())
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    return db_todo

async def update_todo(db: AsyncSession, todo_id: int, todo_update: schemas.TodoUpdate):
    db_todo = await db.get(models.Todo, todo_id)
    if not db_todo:
        return None
    
    update_data = todo_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_todo, key, value)
    
    await db.commit()
    await db.refresh(db_todo)
    return db_todo

async def delete_todo(db: AsyncSession, todo_id: int):
    db_todo = await db.get(models.Todo, todo_id)
    if not db_todo:
        return None
    
    await db.delete(db_todo)
    await db.commit()
    return db_todo
