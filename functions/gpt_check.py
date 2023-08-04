from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
import os

os.environ["OPENAI_API_KEY"] = "YOUR-API-KEY"

chain = ConversationChain(llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1.0), memory=ConversationBufferMemory(return_messages=True))

chain.run('今からあなたには文章を読んでもらいます。その文章をもとに、私を猫化して絵を描いたと仮定して下さい。あくまで仮定です、書く必要はありません。そうしたら、その絵がどんな絵かを説明して下さい。出力は、絵の説明のみ英語で返してください。「ちゃんと野菜とってる偉いっていうのが馬鹿 お前ら もうマジで 死ねんか お前らそういう奴らもできるやろ 野菜は美味しいから食べるんだ ちゃんと野菜食えばいいっていうお前らの考え方がダメ 野菜は美味しいから食う ちゃんと野菜食ってる偉いっていうのはお前らが野菜が嫌いだったからそうなったんだ 死ねば」')

print(chain)