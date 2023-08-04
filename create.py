import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
from datetime import datetime
import openai
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
import io
import warnings
from IPython.display import display
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import matplotlib.pyplot as plt
import json

openai.api_key = "YOUR-API-KEY"
os.environ["OPENAI_API_KEY"] = "YOUR-API-KEY"
os.environ['STABILITY_HOST'] = 'YOUR-HOST'
os.environ['STABILITY_KEY'] = 'YOUR-API-KEY'



# voice --------------------------------------------------------------------

fs = 44100
seconds = 90
myrecording = np.zeros((fs * seconds, 2))

print("\n\nEnter を押すとレコーディング開始されます。(1/5)")
input()

print("レコーディング中です。Enter を押すとレコーディングが終了します。(2/5)")
recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)

try:
    input()
except KeyboardInterrupt:
    pass

sd.stop() 

myrecording = recording[:np.where(recording > 0)[0][-1]]

now = datetime.now()
filename = now.strftime('%Y-%m-%d-%H-%M-%S') + '.wav'
write('voice/'+ filename, fs, myrecording)  
print("レコーディングが完了しました。(3/5)\n")
print("猫化イメージを生成中です。。。。。。(4/5)\n")


# voice to text ----------------------------------------------------------------


def speech_to_text(filepath):
    audio_file= open(filepath, "rb")
    response = openai.Audio.transcribe(model = "whisper-1", file  = audio_file)
    
    return response.text

directory = './voice/'
wav_files = [f for f in os.listdir(directory) if f.endswith('.wav')]
sorted_files = sorted(wav_files, key=lambda x: datetime.strptime(x, '%Y-%m-%d-%H-%M-%S.wav'), reverse=True)
latest_file = sorted_files[0]
raw_text = speech_to_text(directory + latest_file)



# summary ----------------------------------------------------------------


template = PromptTemplate.from_template("今からあなたには文章を読んでもらいます。その文章をもとに、私を猫化して絵を描いたと仮定して下さい。そうしたら、その絵がどんな絵かを説明して下さい。出力は、絵の説明のみ英語で返してください。「{keyword}」")
prompt = template.format(keyword=raw_text)

chat = ChatOpenAI(temperature=0)
output = chat.predict(prompt)




# create image ---------------------------------------------------

stability_api = client.StabilityInference(
    key=os.environ['STABILITY_KEY'], 
    verbose=True, 
    engine="stable-diffusion-v1-5", 
    # Available engines: stable-diffusion-v1 stable-diffusion-v1-5 stable-diffusion-512-v2-0 stable-diffusion-768-v2-0 stable-inpainting-v1-0 stable-inpainting-512-v2-0
    ) 

answers = stability_api.generate(
    prompt=output,
    #seed=992446758, 
    steps=30, 
    cfg_scale=8.0,
    width=512, 
    height=512, 
    samples=1, 
    sampler=generation.SAMPLER_K_DPMPP_2M 
    )


now = datetime.now()
png_name = now.strftime('%Y-%m-%d-%H-%M-%S') + '.png'

for resp in answers:
    for artifact in resp.artifacts:
        if artifact.finish_reason == generation.FILTER:
            warnings.warn(
                "Your request activated the API's safety filters and could not be processed."
                "Please modify the prompt and try again.")
        if artifact.type == generation.ARTIFACT_IMAGE:
            img = Image.open(io.BytesIO(artifact.binary))
            img.save('display/img/' + png_name)
            plt.imshow(img)
            plt.axis('off')
            #plt.show()



# manage json file ------------------------------------------------------------


new_element = {
    "png_name": "{}".format(png_name),
    "raw_text": "{}".format(raw_text),
    "summarised_text": "{}".format(output)
}

# JSONファイルを開いて読み込む
with open('display/data.json', 'r') as f:
    data = json.load(f)

# 要素を追加
data.append(new_element)

# JSONファイルに書き込む
with open('display/data.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


print("猫化イメージが生成されました！探してみてください！(5/5)\n\n")