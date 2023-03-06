import time, sys, os
import speech_recognition as sr
import sounddevice as sd
# import numpy as np
import whisper

print("Loading model", file=sys.stderr)
wmodel = whisper.load_model("base")
print("Model loaded", file=sys.stderr)

DEV = 2


def recognize_whisper(wavfile):
    result = wmodel.transcribe(wavfile, fp16=False)
    # print(result["text"])
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
    txt = recognize_whisper("__spkk__.wav")
    txt = txt.strip()
    print (txt, file=sys.stderr, end="")
    cmd = input().strip()
    if cmd=='q':
        print(txt)
        break
    elif cmd=='x':
        print("\nDELETED", file=sys.stderr)
    elif cmd=='e':
        txt = "replacement theory"
        print (txt, file=sys.stderr)
        print (txt)
    elif cmd == "":
        print(txt, end=" ")
    else:
        txt = txt[:-1] + cmd
        print(txt, file=sys.stderr, end="")
        print (txt)
