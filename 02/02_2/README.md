## [과제 02] FastAPI로 커뮤니티 서비스의 백엔드 구현하기
### ⚒️ Tech Stack
- **Framework** : <img src="https://img.shields.io/badge/FastAPI-05998B?style=flat-square&logo=FastAPI">
- **Database** : <img src="https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite">
- **AI** : <img src="https://img.shields.io/badge/Ollama-000000?style=flat-square&logo=ollama">

## 🌲 프로젝트 구조
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

## 🚀 설치 및 실행 방법
``` ruby
cd 02_2
```
``` ruby
uv sync
```
``` ruby
uv run uvicorn main:app --reload
```

## 📋 API 명세
- **POST /posts** : 글 작성
- **GET /posts** : 글 목록 조회 (닉네임)
- **GET /posts/{post_id}** : 특정 글 조회 (글 번호)
- **PUT /posts/{post_id}** : 글 수정
- **DELETE /posts/{post_id}** : 글 삭제

## 🤔 회고
<details>
<summary>회고입니다</summary>
지금까지 백엔드 개발은 어렵고, 복잡한 영역이라는 생각에 항상 피하기만 했었다. 협업할 때도 늘 다른 팀원이 담당해주기를 바랐고, 스스로 도전할 엄두는 내지 못하고 "백엔드도 한번 해봐야하는데.."라는 생각만 했었다. 이번주 초에 강의를 들으면서도 새로운 개념을 배울 때마다 앞에서 배운 내용을 잊어버리는 모습을 보고 '나는 백엔드와 맞지 않는다'라고 생각하기도 했다.
하지만 이번 과제를 진행하며 이런 생각에서 조금 벗어날 수 있었던 것 같다. 특히, "완벽히 이해하면 좋지만, 우선 코딩을 시작할 수 있는 수준까지만 개념을 익히고 직접 부딪혀봐라"라고 해주신 강사님의 조언이 큰 도움이 되었다. 구글 검색, AI, 노션 교재를 참고하면서 코딩을 시작해보니, 내가 생각했던 것보다 할 수 있는 정도의 내용이었다.
물론.. 이번에도 AI의 도움을 받았지만, 이전보다는 나아진 점이 있다. AI가 만든 코드를 복붙하지 않고 "코드보다 개념을 설명해줘", "더 공부하려면 어떤 키워드로 어떤 자료를 찾아보는게 좋아?"라고 질문하며 주도적으로 학습하려고 노력했다.
100% 혼자만의 힘으로 완성하지 못해서 아쉽지만, AI를 내 공부와 코딩의 가이드로 활용했다는 점에서 스스로 성장했다고 생각한다. 앞으로 매주 과제를 수행하면서 혼자 고민하고 해결하는 개발자가 되기 위해 노력해야겠다.
</details>