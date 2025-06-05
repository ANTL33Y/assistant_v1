# Voice Assistant

An advanced voice assistant built with Python that combines speech recognition, natural language processing, and semantic search capabilities.

## Features

- Real-time speech recognition
- Natural language processing with OpenAI's GPT models
- Semantic search functionality
- Voice response synthesis
- Conversation memory management
- Modular architecture for easy extension

## Requirements

- Python 3.8+
- OpenAI API key
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone [your-repo-url]
cd voice-assistant
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

4. Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

Run the main script:
```bash
python main.py
```

## Project Structure

- `main.py` - Entry point of the application
- `src/`
  - `assistant.py` - Main assistant class
  - `config.py` - Configuration management
  - `llm.py` - Language model integration
  - `memory.py` - Conversation memory management
  - `semantic.py` - Semantic search functionality
  - `voice.py` - Voice input/output handling

## License

MIT License
