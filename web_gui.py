from flask import Flask, render_template, request, jsonify
from src.config import Settings
from src.assistant import PersonalAI
from src.text_voice_io import TextVoiceIO

app = Flask(__name__)

cfg = Settings.load()
voice_io = TextVoiceIO(cfg)
assistant = PersonalAI(cfg, voice_io=voice_io)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json(force=True)
    user_message = data.get('message', '')
    continue_flag = assistant._process(user_message)
    response = voice_io.last_output
    return jsonify({'response': response, 'continue': continue_flag})

if __name__ == '__main__':
    app.run(debug=True)
