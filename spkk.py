import time, sys, os
import speech_recognition as sr
from scipy.io.wavfile import write
import sounddevice as sd

# RCOG = "recognize_google"
RCOG = "recognize_google_cloud"
#RCOG = "recognize_sphinx"
DEV = 2

lastchar = ''

def fixtext(txt):
    global lastchar
    txt = txt.strip()
    if lastchar in ".?!":
        txt = txt.capitalize()
    else:
        txt = txt.lower()
    words = txt.split()
    last = ' '
    for i in range(len(words)):
        if words[i] == "i":
            words[i] = 'I'
        if last[-1] in ".?!":
            words[i] = words[i].capitalize()
        last = words[i]
    if words[-1] == 'colon':
        words.pop(-1)
        words[-1] += ':'
    if words[-1] == 'semicolon':
        words.pop(-1)
        words[-1] += ';'
    txt = " ".join(words)
    lastchar = txt[-1]
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
