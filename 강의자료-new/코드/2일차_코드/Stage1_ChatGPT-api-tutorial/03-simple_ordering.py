from openai import OpenAI
import os

os.environ["OPENAI_API_KEY"] = (
    ""
)

client = OpenAI()

initial_prompt = """
당신은 카페의 친절한 직원입니다.
카페의 메뉴는 다음과 같습니다.
1) 커피, 2) 녹차
각 메뉴에 대하여 1) hot, 2) ice 두 가지 옵션이 있습니다.
처음에는 인사를 하고, 그다음
첫 번째로 커피와 녹차 중 선택해 달라는 질문을 하고, 답변을 받으면 hot과 ice 중 선택해 달라는 질문을 해.
입력받은 후엔 주문 내역을 얘기해줘. 
"""


def ask(question, message_history=[], model="gpt-3.5-turbo"):
    if len(message_history) == 0:
        # 최초 질문
        message_history.append(
            {
                "role": "system",
                "content": initial_prompt,
            }
        )

    # 사용자 질문 추가
    message_history.append(
        {
            "role": "user",
            "content": question,
        },
    )

    # GPT에 질문을 전달하여 답변을 생성
    completion = client.chat.completions.create(
        model=model,
        messages=message_history,
    )

    # 사용자 질문에 대한 답변을 추가
    message_history.append(
        {"role": "assistant", "content": completion.choices[0].message.content}
    )

    return message_history


# 대화 시작
message_history = ask("안녕하세요?", message_history=[])
print(message_history[-1]["content"])
for _ in range(2):
    user_message = input()
    message_history = ask(user_message, message_history=message_history)
    print(message_history[-1]["content"])
