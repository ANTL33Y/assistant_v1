"""Entry point for the voice assistant."""
from src.config import Settings
from src.voice import VoiceIO
from src.assistant import PersonalAI


def main() -> None:
    """Launch the voice assistant from the command line."""
    cfg = Settings.load()
    assistant = PersonalAI(cfg, VoiceIO(cfg))
    assistant.run()


if __name__ == "__main__":
    main()
