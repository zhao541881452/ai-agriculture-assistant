import os
from openai import OpenAI

api_key = os.getenv("API_KEY")

print("当前API_KEY：", api_key)  # 👈 加这一行调试

client = OpenAI(
    api_key=api_key,
    base_url="https://api.siliconflow.cn/v1"
)

# ✅ 普通版本（保留）
def chat_with_llm(messages):
    from rag import search_knowledge

    user_question = messages[-1]["content"]
    knowledge = search_knowledge(user_question)

    system_prompt = f"""
你是一名农业专家，请结合以下知识回答问题：

{knowledge}
"""

    response = client.chat.completions.create(
        model="Qwen/Qwen2.5-7B-Instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            *messages
        ]
    )

    return response.choices[0].message.content


# ✅ 流式版本（新增🔥）
def chat_with_llm_stream(messages):
    from rag import search_knowledge

    user_question = messages[-1]["content"]
    knowledge = search_knowledge(user_question)

    system_prompt = f"""
你是一名农业专家，请结合以下知识回答问题：

{knowledge}
"""

    stream = client.chat.completions.create(
        model="Qwen/Qwen2.5-7B-Instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            *messages
        ],
        stream=True
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
