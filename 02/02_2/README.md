## [과제 02] FastAPI로 커뮤니티 서비스의 백엔드 구현하기
### ⚒️ Tech Stack
<img src="https://img.shields.io/badge/FastAPI-05998B?style=flat-square&logo=FastAPI">
<img src="https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite">
<img src="https://img.shields.io/badge/Ollama-000000?style=flat-square&logo=ollama">

## 프로젝트 구조
``` text
🎁 02
┗ 📦 02_2
  ┣ 📂 routers
  ┃ ┗ 📄 posts.py
  ┣ 📄 controllers.py
  ┣ 📄 database.py
  ┣ 📄 main.py
  ┣ 📄 models.py
  ┗ 📄 web_project.db
```

## 설치 및 실행 방법
``` ruby
cd 02_2
```
``` ruby
uv sync
```
``` ruby
uv run uvicorn main:app --reload
```

## API 명세

## 회고