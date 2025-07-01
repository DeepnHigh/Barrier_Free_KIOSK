from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(dotenv_path="./.env")
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "당신은 파이썬 프로그래머입니다.",
        },
        {
            "role": "user",
            "content": "피보나치 수열을 생성하는 파이썬 프로그램을 작성해주세요.",
        },
    ],
    stream=True,  # 스트림 모드 활성화
)

final_answer = []

# 스트림 모드에서는 completion.choices 를 반복문으로 순회
for chunk in completion:
    # chunk 를 저장
    chunk_content = chunk.choices[0].delta.content
    # chunk 가 문자열이면 final_answer 에 추가
    if isinstance(chunk_content, str):
        final_answer.append(chunk_content)
        # 토큰 단위로 실시간 답변 출력
        print(chunk_content, end="")
