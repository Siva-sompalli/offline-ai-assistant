import speech_recognition as sr

def listen_voice():
    r = sr.Recognizer() 
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except:
        return "Could not understand"
    

