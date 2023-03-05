import time, sys, os
import speech_recognition as sr
import sounddevice as sd
import numpy as np
import whisper

print("Loading model", file=sys.stderr)
wmodel = whisper.load_model("base")
print("Model loaded", file=sys.stderr)

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
    if words[-1] == 'period':
        words.pop(-1)
        words[-1] += '. '
    txt = " ".join(words)
    lastchar = txt[-1]
    return txt


def recognize_whisper(wavfile):
    result = wmodel.transcribe(wavfile, fp16=False)
    print(result["text"])
    return result["text"]

fs = 44100  # Sample rate
seconds = 60  # Duration of recording

print("Enter to start recording", file=sys.stderr)
cmd = input().strip()
while True:
    t = time.time()
    print ("RECORDING...", file=sys.stderr)
    raw = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype="int16")
    cmd = input().strip()
    sd.stop()
    sd.wait()
    t = time.time()-t-.1
    # print (t, "Seconds")
    print ("STOPPED", file=sys.stderr)
    aud = sr.AudioData(raw[:int(t)*fs], fs, 2)
    f=open("__spkk__.wav", 'wb')
    f.write(aud.get_wav_data())
    f.close()
    txt = fixtext(recognize_whisper("__spkk__.wav"))
    print(txt, file=sys.stderr, end="")
    cmd = input().strip()
    if cmd=='q':
        print(txt)
        break
    elif cmd=="":
        print(txt, end=" ")
    else:
        print("\nDELETED", file=sys.stderr)
