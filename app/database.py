import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# 환경 변수로부터 DB URL 로드
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# 1. 비동기 엔진 생성
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False,
    future=True
)

# 2. 비동기 세션 팩토리 생성 (JPA의 EntityManagerFactory 역할)
SessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False, # 커밋 후 객체 만료 방지 (비동기 필수 설정)
)

# 3. 모든 모델의 부모가 될 Base 클래스 (JPA의 @Entity 관리용)
class Base(DeclarativeBase):
    pass

# 4. FastAPI에서 DB 세션을 주입받기 위한 함수 (중요!)
async def get_db():
    async with SessionLocal() as session:
        yield session