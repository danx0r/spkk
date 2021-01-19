import time, sys, os
import speech_recognition as sr
from scipy.io.wavfile import write
import sounddevice as sd

# RCOG = "recognize_google"
RCOG = "recognize_google_cloud"
#RCOG = "recognize_sphinx"
DEV = 2

def fixtext(txt):
    words = txt.strip().capitalize().split()
    for i in range(len(words)):
        if words[i] == "i":
            words[i] = 'I'
    txt = " ".join(words)
    if words[-1].isalnum():
        txt += "."
    return txt

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

print("Enter to start recording", file=sys.stderr)
cmd = input().strip()
while True:
    print ("RECORDING...", file=sys.stderr)
    raw = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype="int16")
    cmd = input().strip()
    sd.stop()
    print ("STOPPED", file=sys.stderr)
    aud = sr.AudioData(raw, 44100, 2)
    txt = fixtext(rcog(aud))
    print(txt, file=sys.stderr, end="")
    cmd = input().strip()
    if cmd=='q':
        print(txt)
        break
    elif cmd=="":
        print(txt, end=" ")
    else:
        print("\nDELETED", file=sys.stderr)
