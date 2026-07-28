# 베이스 이미지: 어떤 바탕에서 시작할지
# Python 3.11이 깔린 깨끗한 리눅스에서 시작하도록 설정
# slim은 가벼운 파이썬 버전
FROM python:3.11-slim

# 상자 안에서 /app 폴더를 작업 공간으로 쓰기
# 파일 복사, 실행 여기서 진행
WORKDIR /app

# 내 requirements.txt를 상자 안(/app)으로 복사
# RUN pip install로 라이브러리 설치
# 캐시 안 남겨서 상자 가볍게 만들기
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 나머지 코드 전부 복사하기
# 현재 폴더의 모든 파일을 상자 안으로 복사
COPY . .

# 포트 알리기
EXPOSE 8000

# 실행 명령
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]