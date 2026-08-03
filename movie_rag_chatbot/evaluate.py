from langsmith import Client
from langsmith.evaluation import evaluate

# rag_langgraph에서 검색에 필요한 것들 가져옴
# gemini 없이 검색하기 위해 안 가져옴
from rag_langgraph import detect_genre, genre_search, vectorstore

# 1. 평가 대상 함수: 질문을 받아서 검색 결과 (영화 제목들)를 반환
def search_target(inputs):
    question = inputs["question"]

    # 장르검색이면 genre_search, 아니면 similarity_search
    g = detect_genre(question)
    if g:
        movies = genre_search(g)
        titles = [m["title_kor"] for m in movies]
    else:
        docs = vectorstore.similarity_search(question, k=5)
        titles = [d.metadata["title_kor"] for d in docs]

    return {"found_titles": titles}

# 2. 평가자: 기대 영화가 검색 결과에 있는지 채점
def correctness(outputs, reference_outputs):
    expected = reference_outputs["expected"]
    found = outputs["found_titles"]

    # 정답 리스트 중 하나라도 검색 결과에 있으면 1점
    score = 0
    
    for exp in expected:
        if any(exp in t or t in exp for t in found):
            score = 1
            break
    return {"key": "search_correct", "score": score}

# 3. 평가 실행
evaluate(
    search_target,
    data="movie-search-eval",
    evaluators=[correctness],
)