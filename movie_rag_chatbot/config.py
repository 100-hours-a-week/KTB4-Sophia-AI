import os
from dotenv import load_dotenv

# 경로 설정
# config.py 있는 폴더가 BASE_DIR
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
CHROMA_DIR = os.path.join(BASE_DIR, "chroma")

# .env 파일 읽어서 토큰 가져오기
load_dotenv()   # .env 파일 읽기
TMDB_TOKEN = os.getenv("TMDB_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")

# 폴더 만들기 (이미 있기는 함)
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(CHROMA_DIR, exist_ok=True)