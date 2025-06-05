# Voice Assistant

An advanced, production-grade voice assistant built with Python. Features modular architecture, plugin system, robust configuration, and extensibility.

## Features

- Real-time speech recognition
- Natural language processing with OpenAI's GPT models
- Semantic search and vector memory
- Voice response synthesis (ElevenLabs, pyttsx3 fallback)
- Conversation memory management
- **Plugin system**: Easily add new skills/tools
- **Advanced configuration**: Supports `.env` and `config.yaml`
- Robust error handling and centralized logging
- Fully type-annotated, documented, and tested

## Requirements

- Python 3.8+
- OpenAI API key
- (Optional) ElevenLabs API key for high-quality TTS
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ANTL33Y/assistant_v1.git
cd assistant_v1
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure your environment:
- Copy `.env.example` to `.env` and fill in your API keys, or
- Create a `config.yaml` for advanced configuration (see below)

## Configuration

The assistant loads configuration from `.env` and/or `config.yaml`, with environment variables taking precedence.

**Example `.env`**
```
OPENAI_API_KEY=your_openai_key
ELEVENLABS_API_KEY=your_elevenlabs_key
```

**Example `config.yaml`**
```yaml
openai_api_key: your_openai_key
elevenlabs_api_key: your_elevenlabs_key
voice_id: AwbZ3Leiit6t97L6NM4u
wake_words:
  - hey assistant
  - hello assistant
  - assistant
max_interactions: 100
ambient_adjust_sec: 0.5
listen_timeout: 10
phrase_time_limit: 7
```

## Plugin System

Add new skills by dropping plugin files into `src/plugins/`. Each plugin should inherit from `AssistantPlugin` and register its commands.

**Example:**
```python
from src.plugins.base import AssistantPlugin

class WeatherPlugin(AssistantPlugin):
    name = "Weather"
    description = "Provides weather information."

    def register(self):
        return {"weather": self.handle_weather}

    def handle_weather(self, command: str, *args, **kwargs):
        return "The weather is sunny and 25°C."
```

### Built-in Reminder Plugin

This repository also ships with a simple `ReminderPlugin` allowing you to schedule spoken reminders.
Use a command such as:

```
remind me to buy milk at 6pm
```

The assistant will speak the reminder at the requested time while running.

## Usage

Run the main script:
```bash
python main.py
```

## Project Structure

- `main.py` - Entry point
- `src/`
  - `assistant.py` - Main assistant class
  - `config.py` - Configuration management
  - `llm.py` - Language model integration
  - `memory.py` - Conversation memory
  - `semantic.py` - Semantic search
  - `voice.py` - Voice I/O
  - `logging.py` - Centralized logging
  - `plugins/` - Plugin system

## Testing

Tests are located in the `tests/` directory. Run with:
```bash
pytest
```

## License

MIT License
