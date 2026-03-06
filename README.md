# sfacspace-todo-assignment

# 🐳 FastAPI Async Todo REST API

본 프로젝트는 **FastAPI**와 **PostgreSQL**을 기반으로 한 비동기 할 일 관리(Todo) 서버입니다.  
Docker 환경에서 인프라를 구축하고, SQLAlchemy 2.0의 비동기 기능을 활용하여 효율적인 데이터 처리를 구현했습니다.

---

## 🛠 Tech Stack
- **Framework**: FastAPI (Python 3.11)
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0 (Async Mode)
- **Driver**: asyncpg
- **Infrastructure**: Docker, Docker Compose

---

## 🏗 프로젝트 구조
```text
todo-api/
├── app/
│   ├── main.py         # FastAPI 앱 진입점 및 Lifespan(DB 초기화) 설정
│   ├── models.py       # SQLAlchemy ORM 모델 정의
│   ├── schemas.py      # Pydantic DTO (입출력 검증)
│   ├── database.py     # 비동기 DB 엔진 및 세션 설정
│   └── routers/
│       └── todos.py    # Todo CRUD 비동기 라우터
├── Dockerfile          # API 서버 이미지 빌드 설정
├── docker-compose.yml  # API, DB, pgAdmin 컨테이너 오케스트레이션
├── .env                # 환경 변수 (DB 접속 정보 등)
└── README.md           # 프로젝트 문서
🚀 실행 방법
1. 환경 변수 설정
프로젝트 루트에 .env 파일을 생성하고 아래 내용을 입력합니다. (비동기 드라이버 +asyncpg 필수)

코드 스니펫
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/todo_db
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=todo_db
2. 컨테이너 빌드 및 실행
Bash
docker-compose up --build -d
3. API 확인
Swagger UI: http://localhost:8000/docs

Health Check: http://localhost:8000/health
todo-Rest Api 서버 구축 과제
기간 3월 9일
스택 : python 3.11 / FastAPI / PostgreSQL / Docker / Dokcer Compose
목표 : Dokcer와 python을 이용해 실제로 동작하는 REST API 서버 구축
포트 / ip / 웹 서버 / 컨테이너 네트워크 개념을 손으로 경험 하는것이 핵심

생각해볼것 api 컨테이너 DB에 접속할 때 host를 localhost로 하면 왜 안될까요?
docker 환경에서 localhost는 자기자신(컨테이너)를 의미합니다
api컨테이너 내부에서 localhost를 찾으면 api 컨테이너 내부에서 db를 찾게됩니다 하지만 요구사항은 별도의 컨테이너에서 db가 돌고 있기때문에 localhost를 통해 접속하려고 하면 문제가 발생합니다

바인딩 주소 실험
127.0.0.1 은 루프백 을 의미한다
컨테이너 내부 서버가 이 컨테이너 안에서 발생하는 요청만 받겠다 라고 선언한 상태
왜 안될까? 호스트 pc의 브라우저는 컨테이너 입장에서 보면 외부망이다 포트 포워딩을 통해 요청이 컨테이너 대문까지는 도착하지만 서버 엔진이 나는 내부 요청만 받기로 했으니 거절하겠다 라며 요청을 반려함

0.0.0.0 은 모든 네트워크 인터페이스를 의미한다
컨테이너가 가진 가상 랜카드로 들어오는 모든 요청을 수라하겠다라는 뜻 따라서 호스트 pc나 다른 네트워크의 요청이 정상적으로 애플리케이션까지 도달한다
도커 포트포워딩이나 ec2 외부 접속을 처리하려면 서버가 모든 경로의 요청을 수락할 수 있도록 바인딩 필요
