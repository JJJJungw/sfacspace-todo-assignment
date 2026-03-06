from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import engine, Base
from .routers import todos

# [1단계] Lifespan 설정: 앱 시작 시 테이블 생성
# 비동기 엔진은 run_sync를 통해서만 create_all을 실행할 수 있습니다.
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        # 이 코드는 앱이 시작될 때 테이블이 없으면 생성해줍니다.
        await conn.run_sync(Base.metadata.create_all)
    yield
    # 앱 종료 시 수행할 작업이 있다면 여기에 작성 (예: DB 연결 종료)

app = FastAPI(
    title="Todo assignment API",
    description="FastAPI + PostgreSQL Todo 리스트 서비스",
    version="1.0.0",
    lifespan=lifespan  # lifespan 등록
)

@app.get("/health", tags=["api"])
async def health_check():  # async 추가
    return {"status": "ok", "message": "정상작동"}

@app.get("/", tags=["api"])
async def read_root():  # async 추가
    return {"message": "Todo API"}

app.include_router(todos.router)