from flask import Flask, render_template, request
import engine.stt as stt
import engine.llm as llm
import engine.tts as tts

tts.init()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_audio', methods=['POST'])
def process_audio():
    try:
        question = stt.speech_to_text()
        response = llm.llm(question=question)

        # Text response
        text_response = f"Question: {question}\nResponse: {response}"

        # Audio response
        tts.text_to_speech(text_response)

        return render_template('index.html', question=question, response=response, text_response=text_response)
    
    except RuntimeError:
        # Restart the speech recognition loop
        return render_template('index.html', error="RuntimeError occurred. Please try again.")

if __name__ == '__main__':
    app.run(debug=True)
