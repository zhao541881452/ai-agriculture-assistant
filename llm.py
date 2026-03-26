import os
from openai import OpenAI

api_key = os.getenv("API_KEY")

print("当前API_KEY：", api_key)  # 👈 加这一行调试

client = OpenAI(
    api_key=api_key,
    base_url="https://api.siliconflow.cn/v1"
)

def chat_with_llm(messages):
    response = client.chat.completions.create(
        model="Qwen/Qwen2.5-7B-Instruct",
        messages=messages
    )
    return response.choices[0].message.content



def chat_with_llm_stream(messages):
    stream = client.chat.completions.create(
        model="Qwen/Qwen2.5-7B-Instruct",
        messages=messages,
        stream=True
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
