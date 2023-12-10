
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import speech_recognition as sr
import pyttsx3
from langchain.llms import GooglePalm
from langchain.prompts import PromptTemplate
from langchain import LLMChain

app = Flask(__name__)
socketio = SocketIO(app)

# Set up the LLMChain, GooglePalm, and PromptTemplate
api_key = 'AIzaSyCG1msBTRTQdLSQfU9JpN6KVrGG3nPRswM'
llm = GooglePalm(google_api_key=api_key, temperature=0.1)

prompt_template = 'consider yourself as Chacha Chaudhary, a comic character who is the mascot of the Namami Gange Project who will welcome the user with Namaste and supposed to impart knowledge about rivers, conservation, and all. Try to remain casual while talking as most users will be children and young people. also provide relevant links of sources. Avoid all irrelevant questions not related to Ganga and rivers. Make sure not to answer irrelevant questions by saying, "let us try to stick to the topic of Ganga and NMCG, you can ask me anything related to that. Now, answer the following question: {question}'

prompt = PromptTemplate.from_template(prompt_template)
llm_chain = LLMChain(prompt=prompt, llm=llm)

# Function for text-to-speech
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Web route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Web socket route for processing the user's input
@socketio.on('process_input')
def process_input(data):
    user_input = data['user_input']
    question = user_input

    # Use LLMChain to get the response
    response = llm_chain.run({"question": question})

    # Convert the response to speech
    text_to_speech(response)

    # Emit the response to the client
    emit('response', {'response': response})

if __name__ == '__main__':
    socketio.run(app, debug=True)
