from fastapi import FastAPI
from .database import engine
from . import models
from .routers import todos
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Todo assignment API",
    description="FastAPI + PostgreSQL Todo 리스트 서비스",
    version="1.0.0"
)

@app.get("/health", tags=["api"])
def health_check():
    return {"status": "ok", "message": "정상작동"}

@app.get("/", tags=["api"])
def read_root():
    return {"message": "Todo API"}

app.include_router(todos.router)