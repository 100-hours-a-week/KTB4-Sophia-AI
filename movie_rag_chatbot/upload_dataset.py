import json
from dotenv import load_dotenv

load_dotenv()

from langsmith import Client

client = Client()

# jsonl 읽기
examples = []
with open("movie-search-eval.jsonl", encoding="utf-8") as f:
    for line in f:
        row = json.loads(line)
        examples.append(row)

# 데이터셋 만들기 (이름 겹치면 에러나니까 새 이름 or 기존 이름 삭제하기)
dataset = client.create_dataset("movie-search-eval")

# 업로드
client.create_examples(
    inputs=[{"question": e["question"]} for e in examples],
    outputs=[{"expected": e["expected"]} for e in examples],
    dataset_id=dataset.id,
)
print("업로드 완료: ", len(examples), "개")