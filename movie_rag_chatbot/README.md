# 🎬 Movie RAG Chatbot (ASKFLIX)

스포일러 수위를 조절할 수 있는 영화 정보 검색 및 추천 챗봇 (RAG 기반)

---

## 💡 기획 배경

평소 영화를 틀어놓고 다른 일을 하다 보면 내용을 놓쳐 다시 보거나 꺼버리는 일이 많았다.
그래서 좋아하는 장르를 골라 검색하고 줄거리를 미리 파악한 뒤 편하게 감상할 수 있는 도구가 있으면 좋겠다고 생각했다.
스마트 TV에 "영화 추천해줘"라고 하면 대개 평점이나 인기 상위작만 보여주는데, 사용자의 요청 (장르, 분위, 소재)에 맞춰 필터링해 추천해주는 챗봇이 있으면 더 유용하겠다고 생각했다.
다만, 줄거리를 미리 알고 보기를 원하는 사람도 있고, 스포일러를 싫어하는 사람도 있어서 스포일러 수위를 사용자가 조절할 수 있도록 만들었다.

---

## 🛠️ 기술 스택

- **LLM / 임베딩**: Google Gemini (`gemini-flash-latest`, `gemini-embedding-001`)
- **벡터 DB**: ChromaDB
- **프레임워크**: LangChain (LCEL), LangGraph (StateGraph)
- **추적 및 모니터링**: LangSmith
- **데이터 출처**: TMDB API, 위키백과 API
- **백엔드**: FastAPI (REST API), Uvicorn
- **프론트엔드**: HTML / CSS / JavaScript
- **배포**: Docker, docker-compose, AWS EC2

---

## 📁 프로젝트 구성

**공통** ✅ 완료
- `config.py`: 경로, API 키 설정
- `collect_data.py`: TMDB, 위키백과에서 영화 데이터 수집 -> movies.jsonl
- `build_index.py`: 데이터를 청킹 및 임베딩해 ChromaDB에 저장
- `fill_plots.py`: 빈 줄거리만 골라 위키백과에서 재수집해 보강
- `add_directors.py`: TMDB 데이터 항목 중 'crew'에서 감독 정보를 수집해 추가
- `inspect_data.py`: 수집 데이터 점검용 파일 (json -> csv 변환, 장르별 개수 확인)

**RAG 3 버전** ✅ 완료
- `rag.py`, `app.py`: 바닐라 RAG
- `rag_langchain.py`, `app_langchain.py`: LangChain (LCEL)
- `rag_langgraph.py`, `app_langgraph.py`: LangGraph (메인 버전)

**웹 서비스, 배포** ✅ 완료
- `api.py` - FastAPI 서버. `/chat`, `/chat`, `/chat/stream`, 프론트
- `index.html` - 웹 프론트엔드 (넷플릭스 스타일 채팅 UI, ASKFLIX)
-  `Dockerfile`, `docker-compose.yml`: 컨테이너 빌드, 실행 설정

---

## ▶️ 실행 방법

**1. 환경 설정**
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```
`.env` 생성 후 `TMDB_TOKEN`, `GEMINI_API_KEY` 입력하기

**2. 데이터, 인덱스 준비**
```bash
python collect_data.py
python build_index.py
```

**3. 실행**
```bash
# CLI
python app_langgraph.py
# 웹 (로컬)
uvicorn api:app --reload
# 웹 (Docker)
docker compose up --build
```

**LangSmith 추적** - `.env`에 추가
```
LANGSMITH_TRACING=true
LANGSMITH_API_KEY
LANGSMITH_PROJECT=movie-rag-chatbot
```

## 🚀 배포

Docker 컨테이너로 AWS EC2에 배포. FastAPI가 프론트까지 서빙하는 단일 컨테이너 구조
```bash
# EC2에서
git clone <repo> && cd movie_rag_chatbot
# .env 생성 후
docker compose up --build -d
```

---

## 📚 개발 기록

프로젝트 진행 과정과 상세 기록은 `history/` 폴더 참고!
- [진행 상황 및 계획](./history/ROADMAP.md)
- [트러블슈팅](./history/TROUBLESHOOTING.md)
- [회고](./history/RETROSPECTIVE.md)