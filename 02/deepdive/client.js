// 주소 뒤에 내가 원하는 작업: 추론(predict)
fetch('http://127.0.0.1:8000/predict', {
    // 데이터를 서버로 보낼거임
    method: 'POST',
    // 어떤 형식? 서버에게 내가 보내는 데이터는 JSON 형식이라고 알려줌
    headers: { 'Content-Type': 'application/json' },
    // 무슨 내용? 실제 보낼 데이터(문자열)
    body: JSON.stringify({ age: "20" })
})
// 응답 확인: 서버가 준 응답(JSON)을 자바스크립트가 쓸 수 있게
.then(response => response.json())
// 서버에서 준 결과를 콘솔에 출력
.then(data => console.log(data))
// 예외 처리: 에러 내용 출력
.catch(error => console.error('Error:', error));