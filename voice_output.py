import pyttsx3
import threading

# 🎤 Speak function
def speak(text):

    def run():
        try:
            engine = pyttsx3.init()   # ✅ new engine every time

            engine.setProperty("rate", 170)

            voices = engine.getProperty("voices")
            if voices:
                engine.setProperty("voice", voices[0].id)

            engine.say(text)
            engine.runAndWait()
            engine.stop()

        except Exception as e:
            print("Voice Error:", e)

    # ✅ run in background thread
    threading.Thread(target=run, daemon=True).start()


# 🔇 Stop manually
def stop_speaking():
    try:
        engine = pyttsx3.init()
        engine.stop()
    except:
        pass