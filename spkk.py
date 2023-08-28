import time, sys, os
import speech_recognition as sr
import sounddevice as sd
import whisper

fs = 44100  # Sample rate
seconds = 60  # Duration of recording

for DEV, dev in enumerate(sd.query_devices()):
    if "AK5370" in dev['name']:
        print ("Setting DEV=", DEV)

print("Loading model")
wmodel = whisper.load_model("base")
print("Model loaded")

def recognize_whisper(wavfile):
    result = wmodel.transcribe(wavfile, fp16=False)
    return result["text"]

print("Enter to start recording")
cmd = input().strip()
fout = open(sys.argv[1], 'a')

while True:
    t = time.time()
    print ("RECORDING...")
    raw = sd.rec(int(seconds * fs), samplerate=fs, channels=1, device=DEV, dtype="int16")
    input()
    sd.stop()
    sd.wait()
    t = time.time()-t-.1
    print ("STOPPED")
    aud = sr.AudioData(raw[:int(t)*fs], fs, 2)
    f=open("__spkk__.wav", 'wb')
    try:
        f.write(aud.get_wav_data())
    except:
        f.close()
        print("ERROR -- <enter> to resume recording, 'q' to quit")
        cmd = input()
        if cmd[:1] == 'q':
            break
        continue
    f.close()
    txt = recognize_whisper("__spkk__.wav")
    txt = txt.strip()
    print (txt, end="")
    cmd = input()
    if cmd[:1] == ' ':
        cmd = ' '
    else:
        cmd = cmd.strip()
    if cmd=='q':
        print(txt, file=fout)
        break
    elif cmd=='x':
        print("\nDELETED")
    elif cmd=='e':
        f = open("__spkk_edit__", 'w')
        f.write(txt)
        f.close()
        os.system("nano __spkk_edit__")
        f = open("__spkk_edit__")
        txt = f.read()
        f.close()
        print (txt, file=fout)
        print (txt)
    elif cmd == "":
        print(txt, end=" ", file=fout)
    else:
        txt = txt[:-1] + cmd
        print (txt, file=fout)
        print(txt, end="")
