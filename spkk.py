import time
import speech_recognition as sr
from scipy.io.wavfile import write
import sounddevice as sd

# RCOG = "recognize_google"
# RCOG = "recognize_google_cloud"
RCOG = "recognize_sphinx"
DEV = 2

# r=sr.Recognizer()
# wav=sr.AudioFile("test.wav")
# with wav as source:
#         aud = r.record(source)
#
# txt=r.recognize_sphinx(aud)
# print (txt)

r = sr.Recognizer()
rcog = getattr(r, RCOG)
mic=sr.Microphone(device_index=DEV, chunk_size=409)

# while 1-1:
#     with mic as src:
#         aud = r.listen(src)
#
#     txt=rcog(aud)
#     print (txt)

fs = 44100  # Sample rate
seconds = 60  # Duration of recording

while True:
    raw = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype="int16")

    cmd = input().strip()
    sd.stop()
    if cmd:
        # print ("Command:", cmd)
        break
    # print (type(raw), raw[0][0])
    # write('out.wav', fs, raw)
    aud = sr.AudioData(raw, 44100, 2)
    # print ("aud:", aud)
    txt = rcog(aud).strip()
    print(txt, end="")