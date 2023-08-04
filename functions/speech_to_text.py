import openai
import os
from datetime import datetime
openai.api_key = "YOUR-API-KEY"



def speech_to_text(filepath):
    audio_file= open(filepath, "rb")
    response = openai.Audio.transcribe(model = "whisper-1", file  = audio_file)
    
    return response.text


directory = './voice/'
wav_files = [f for f in os.listdir(directory) if f.endswith('.wav')]
sorted_files = sorted(wav_files, key=lambda x: datetime.strptime(x, '%Y-%m-%d-%H-%M-%S.wav'), reverse=True)
latest_file = sorted_files[0]
text = speech_to_text(directory + latest_file)

print(text)

