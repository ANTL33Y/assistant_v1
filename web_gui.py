from flask import Flask, render_template, request, jsonify
from src.config import Settings
from src.assistant import PersonalAI
from src.text_voice_io import TextVoiceIO
from src.voice import VoiceIO


class WebVoiceIO(TextVoiceIO):
    """Voice I/O that stores output for the GUI and speaks it."""

    def __init__(self, settings) -> None:
        super().__init__(settings)
        self._voice = VoiceIO(settings)

    def speak(self, text: str) -> None:
        super().speak(text)
        self._voice.speak(text)

app = Flask(__name__)

cfg = Settings.load()
voice_io = WebVoiceIO(cfg)
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


@app.route('/history')
def history():
    interactions = []
    for inter in assistant.memory.data.get('interactions', []):
        if inter['type'] in ('user_command', 'ai_response'):
            interactions.append({
                'type': 'user' if inter['type'] == 'user_command' else 'ai',
                'content': inter['content']
            })
    return jsonify(interactions)

if __name__ == '__main__':
    app.run(debug=True)
