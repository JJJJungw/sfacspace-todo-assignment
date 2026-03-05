# sfacspace-todo-assignment

todo-Rest Api 서버 구축 과제
기간 3월 9일
스택 : python 3.11 / FastAPI / PostgreSQL / Docker / Dokcer Compose
목표 : Dokcer와 python을 이용해 실제로 동작하는 REST API 서버 구축
포트 / ip / 웹 서버 / 컨테이너 네트워크 개념을 손으로 경험 하는것이 핵심

생각해볼것 api 컨테이너 DB에 접속할 때 host를 localhost로 하면 왜 안될까요?
docker 환경에서 localhost는 자기자신(컨테이너)를 의미합니다
api컨테이너 내부에서 localhost를 찾으면 api 컨테이너 내부에서 db를 찾게됩니다 하지만 요구사항은 별도의 컨테이너에서 db가 돌고 있기때문에 localhost를 통해 접속하려고 하면 문제가 발생합니다
