from langsmith import Client
from langsmith.evaluation import evaluate

# 1. 평가 대상 함수: 질문을 받아서 검색 결과 (영화 제목들)를 반환
def search_target(inputs):
    question = inputs["question"]
    # 검색된 영화 제목 리스트 반환
    return {"found_titles": [...]}

# 2. 평가자: 기대 영화가 검색 결과에 있는지 채점
def correctness(outputs, reference_outputs):
    expected = reference_outputs["expected"]
    found = outputs["found_titles"]
    # expected가 found 안에 있으면 1점, 없으면 0점
    return {"key": "search_correct", "score": ...}

# 3. 평가 실행
evaluate(
    search_target,
    data="movie-search-eval",
    evaluators=[correctness],
)