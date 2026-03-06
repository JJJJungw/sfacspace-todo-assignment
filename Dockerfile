FROM python:3.11-slim-bookworm

# uv 바이너리 가져오기
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# 1. 의존성 파일 먼저 복사
COPY pyproject.toml uv.lock ./

# 2. 패키지 설치 (가상환경을 컨테이너 루트 시스템에 직접 설치하도록 설정하거나 명시적 생성)
RUN uv sync --frozen --no-cache

# 3. 소스 코드 복사
COPY . .

# 4. PATH 설정 (uv sync는 기본적으로 /app/.venv를 만듭니다)
ENV PATH="/app/.venv/bin:$PATH"

# 5. 실행 명령
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]