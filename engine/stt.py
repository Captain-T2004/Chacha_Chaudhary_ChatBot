import speech_recognition as sr

def speech_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something:")
        audio = recognizer.listen(source,timeout=5)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None