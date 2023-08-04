import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
from datetime import datetime




fs = 44100
seconds = 90
myrecording = np.zeros((fs * seconds, 2))

print("Press Enter to start recording.")
input()

print("Recording started. Press Enter to stop recording.")
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
print("Recording has been saved as output.wav.")
