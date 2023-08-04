from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
os.environ["OPENAI_API_KEY"] = "YOUR-API-KEY"




template = PromptTemplate.from_template("今からあなたには文章を読んでもらいます。その文章をもとに、私を猫化して絵を描いたと仮定して下さい。そうしたら、その絵がどんな絵かを説明して下さい。出力は、絵の説明のみ英語で返してください。「{keyword}」")
prompt = template.format(keyword=input())

chat = ChatOpenAI(temperature=0)
output = chat.predict(prompt)

print(output)
