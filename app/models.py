# 파이썬에서 보면적으로 사용하는 orm은 sqlalchemy 가 있다
# 이 alchemy는 core방식과 orm방식이 있는데 지금은 orm 방식을 채택하려고 한다 기존에 사용했던 jpa와 비슷한 형식이라고 판단이 들어 선택하게 되었다
# 선언 방식에서 부터 차이점이 존재하는데 하나씩 알아보자
# from sqlalchemy import create_engine, MetaData, Table, select => core 방식에서는 선언시 직접적인 객체를 사용한다(meta data 등등..)

#현재 orm방식은 일반적으로 declarativeBase상위 클래스를 상속받아 클래스를 생성하는것이다. (공식문서 2.0.48 기준)
from datetime import datetime
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class Todo(Base):
    __tablename__ = "todos"

    # Python 3.10+ 스타일: Optional 대신 T | None 사용 가능 (SQLAlchemy 매핑에서도 인식됨)
    id: Mapped[int] = mapped_column(primary_key=True) # Integer 생략 가능 (Mapped[int]로 추론)
    title: Mapped[str] = mapped_column(String(255))  # nullable=False는 기본값 (Mapped[str] 기준)
    description: Mapped[str | None] = mapped_column(String(500)) # Optional[str] 대신 str | None
    is_done: Mapped[bool] = mapped_column(default=False)
    
    # server_default는 DB 레벨의 기본값, default는 Python 레벨의 기본값
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
