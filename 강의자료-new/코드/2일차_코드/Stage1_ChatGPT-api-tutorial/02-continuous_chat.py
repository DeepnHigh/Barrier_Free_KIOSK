import os
from openai import OpenAI

os.environ["OPENAI_API_KEY"] = (
    ""
)

client = OpenAI()


def ask(question, message_history=[], model="gpt-3.5-turbo"):
    if len(message_history) == 0:
        # 최초 질문
        message_history.append(
            {
                "role": "system",
                "content": "You are a helpful assistant. You must answer in Korean.",
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


# 최초 질문
message_history = ask("양자역학에 대해서 쉽게 설명해 주세요", message_history=[])
# 최초 답변
print(message_history[-1]["content"])
print("--------------------------------")
# 두 번째 질문
message_history = ask(
    "이전의 내용을 영어로 답변해 주세요", message_history=message_history
)
# 두 번째 답변
print(message_history[-1]["content"])
