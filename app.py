from flask import Flask, render_template, request
import speech_recognition as sr
from langchain.llms import GooglePalm
from langchain.prompts import PromptTemplate
from langchain import LLMChain
import pyttsx3

app = Flask(_name_)

api_key = 'AIzaSyCG1msBTRTQdLSQfU9JpN6KVrGG3nPRswM'
llm = GooglePalm(google_api_key=api_key, temperature=0.1)
prompt_template = 'answer the following question: {question}'
prompt = PromptTemplate.from_template(prompt_template)
llm_chain = LLMChain(prompt=prompt, llm=llm)

engine = pyttsx3.init()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_audio', methods=['POST'])
def process_audio():
    try:
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Say something...")
            audio = recognizer.listen(source, timeout=5)

        question = recognizer.recognize_google(audio)
        response = llm_chain.run({"question": question})

        # Text response
        text_response = f"Question: {question}\nResponse: {response}"

        # Audio response
        engine.say(text_response)
        engine.runAndWait()

        return render_template('index.html', question=question, response=response, text_response=text_response)

    except sr.UnknownValueError:
        return render_template('index.html', error="Sorry, could not understand audio.")
    except sr.RequestError as e:
        return render_template('index.html', error=f"Could not request results from Google Speech Recognition service; {e}")
    except RuntimeError:
        # Restart the speech recognition loop
        return render_template('index.html', error="RuntimeError occurred. Please try again.")

if _name_ == '_main_':
    app.run(debug=True)
