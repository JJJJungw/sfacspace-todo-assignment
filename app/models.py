# 파이썬에서 보면적으로 사용하는 orm은 sqlalchemy 가 있다
# 이 alchemy는 core방식과 orm방식이 있는데 지금은 orm 방식을 채택하려고 한다 기존에 사용했던 jpa와 비슷한 형식이라고 판단이 들어 선택하게 되었다
# 선언 방식에서 부터 차이점이 존재하는데 하나씩 알아보자
# from sqlalchemy import create_engine, MetaData, Table, select => core 방식에서는 선언시 직접적인 객체를 사용한다(meta data 등등..)

#현재 orm방식은 일반적으로 declarativeBase상위 클래스를 상속받아 클래스를 생성하는것이다. (공식문서 2.0.48 기준)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, Integer, Boolean, func

class Base(DeclarativeBase):
    pass
#현재는 Mapped를 사용해서 테이블을 만들고 있는 추세
class Todo(Base):
    __tablename__ = "todos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_done: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
