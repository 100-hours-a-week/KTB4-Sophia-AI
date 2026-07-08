from rag import answer

# 테스트 질문
# print(answer("우주를 배경으로 한 SF 영화 추천해줘"))
# print(answer("인셉션 줄거리 결말까지 알려줘", spoiler_free=False))

print("=== 챗봇 시작! ===")
print("종료하려면 '종료'를 입력하세요")

while True:
    user_input = input("나: ")
    if user_input == '종료':
        break
    # 결말/스포/줄거리 요청이면 스포일러 검색까지 하기
    wants_spoiler = any(word in user_input for word in ["결말", "스포", "줄거리"])
    print("답변: ", answer(user_input))