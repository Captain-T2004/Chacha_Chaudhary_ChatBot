from flask import Flask, render_template, request, jsonify
import engine.llm as llm
import engine.tts as tts

tts.init()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def process_audio():
    try:
        question = request.get_json()['question']
        response = llm.llm(question=question)
        text_response = f"Response: {response}"
        print(text_response)
        return jsonify(result=text_response)
    
    except RuntimeError:
        return render_template('index.html', error="RuntimeError occurred. Please try again.")

if __name__ == '__main__':
    app.run(debug=True)
