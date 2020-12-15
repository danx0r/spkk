import speech_recognition as sr

r=sr.Recognizer()
wav=sr.AudioFile("test.wav")
with wav as source:
        aud = r.record(source)

txt=r.recognize_sphinx(aud)
print (txt)
