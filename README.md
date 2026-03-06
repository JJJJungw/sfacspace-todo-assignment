#  FastAPI  Todo REST API

본 과제는 FastAPI와 PostgreSQL을 기반으로 한 할 일 관리(Todo) 서버입니다. Docker 컨테이너 환경에서 인프라를 구축하고, SQLAlchemy를 활용하여 데이터 처리를 구현했습니다.

---

## Tech Stack
- Framework: FastAPI (Python 3.11)
- Database: PostgreSQL 15
- ORM: SQLAlchemy
- Driver: asyncpg
- Infrastructure: Docker, Docker Compose

---

##  프로젝트 구조
```text
todo-api/
├── app/
│   ├── main.py         # FastAPI 앱 진입점 및 DB 초기화 설정
│   ├── models.py       # SQLAlchemy ORM 모델 정의
│   ├── schemas.py      # Pydantic DTO
│   ├── database.py     # 비동기 DB 엔진 및 세션 설정
│   └── routers/
│       └── todos.py    # Todo CRUD 라우터
├── Dockerfile          # API 서버 이미지 빌드 설정
├── docker-compose.yml  # API, DB, pgAdmin 컨테이너 오케스트레이션
├── .env                # 환경 변수
└── README.md           # 프로젝트 문서
```
## 실행 방법

### 1. 환경 변수 설정
프로젝트 루트에 `.env` 파일을 생성하고 아래 내용을 입력합니다.

```env
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/todo_db
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=todo_db
```
### 2. 컨테이너 빌드 및 실행
터미널에서 아래 명령어를 입력하여 서비스를 빌드하고 백그라운드에서 실행합니다.

```bash
docker-compose up --build -d
```

### 3.API 확인
컨테이너가 정상적으로 실행되면 브라우저를 통해 아래 주소에서 API를 확인하고 테스트할 수 있습니다.
```link
Swagger UI (자동 문서화): http://localhost:8000/docs

Health Check (상태 확인): http://localhost:8000/health
```
### 1. localhost(127.0.0.1)와 0.0.0.0의 차이

* localhost (127.0.0.1)**: '루프백(Loopback)' 주소로, **자기 자신**만을 가리킵니다. 컨테이너 내부에서 서버를 `localhost`로 띄우면, 컨테이너 밖(호스트 PC)이나 다른 컨테이너에서는 이 서버에 접속할 수 없습니다.
* 0.0.0.0: 서버의 **모든 네트워크 인터페이스**를 개방한다는 의미입니다. 도커 환경에서 서버를 `0.0.0.0`으로 바인딩해야만 호스트의 포트 포워딩을 통해 외부 요청을 받을 수 있습니다.
* 포인트: "내 로컬 PC 브라우저에서 접속하려면 컨테이너는 모든 문(0.0.0.0)을 열어두어야 한다"
* api 컨테이너 DB에 접속할 때 host를 localhost로 하면 왜 안될까?
** docker 환경에서 localhost는 자기자신(컨테이너)를 의미
** api컨테이너 내부에서 localhost를 찾으면 api 컨테이너 내부에서 db를 찾게됩니다
** 별도의 컨테이너에서 db가 돌고 있기때문에 localhost를 통해 접속하려고 하면 문제가 발생


바인딩 주소 실험
127.0.0.1 은 루프백 을 의미한다
컨테이너 내부 서버가 이 컨테이너 안에서 발생하는 요청만 받겠다 라고 선언한 상태
왜 안될까? 호스트 pc의 브라우저는 컨테이너 입장에서 보면 외부망이다 포트 포워딩을 통해 요청이 컨테이너 대문까지는 도착하지만 서버 엔진이 나는 내부 요청만 받기로 했으니 거절하겠다 라며 요청을 반려함


---

### 2. db:5432 접속이 가능한 이유 (Docker Networking)

* **Docker DNS**: Docker Compose로 실행된 컨테이너들은 자동으로 하나의 가상 네트워크(Bridge Network)에 소속됩니다. 
* **서비스 이름 확인**: 도커는 내부적으로 **Embedded DNS Server**를 가지고 있어, `docker-compose.yml`에 정의된 서비스 이름(`db`)을 해당 컨테이너의 내부 IP 주소로 자동 변환(Name Resolution)해줍니다.
* **학습 포인트**: 별도의 고정 IP 설정 없이도 서비스 이름만으로 컨테이너 간 통신이 가능한 '서비스 디스커버리'의 편리함을 확인했습니다.



---

### 3. Docker Volume이 없을 때 컨테이너 재시작 시 발생하는 일

* **데이터 유실 (Ephemerality)**: 컨테이너는 기본적으로 '휘발성'입니다. 컨테이너 내부 쓰기 계층(Writable Layer)에 저장된 데이터는 컨테이너가 **삭제(down)**되는 순간 함께 사라집니다.
* **Volume의 역할**: 호스트의 특정 폴더와 컨테이너 내부의 데이터 폴더를 동기화하여, 컨테이너가 교체되거나 삭제되어도 실제 데이터(DB 파일 등)는 유지되도록 합니다.
* **학습 포인트**: 스테이트풀(Stateful)한 DB 서비스에서 볼륨 설정은 선택이 아닌 필수임을 깨달았습니다.



---

### 4. /health 엔드포인트의 실제 서비스 필요성

* **상태 확인 (Liveness/Readiness Probe)**: 운영 환경(AWS ALB, Kubernetes 등)에서 오케스트레이터가 서버의 생존 여부를 주기적으로 체크합니다.
* **자동 복구**: 만약 `/health` 응답이 실패하면 로드밸런서는 해당 인스턴스로 트래픽을 보내지 않거나, 컨테이너를 자동으로 재시작하여 서비스 가용성을 유지합니다.
* **학습 포인트**: 단순히 기능 구현을 넘어, 운영 단계에서의 안정성을 위해 헬스체크 API가 표준임을 배웠습니다.

---


