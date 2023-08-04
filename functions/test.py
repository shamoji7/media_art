import os
import openai

os.environ["OPENAI_API_KEY"] = "YOUR-API-KEY"
openai.api_key = os.environ["OPENAI_API_KEY"]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "日本の総理大臣は誰ですか？"},
    ],
)
print(response.choices[0]["message"]["content"].strip())
