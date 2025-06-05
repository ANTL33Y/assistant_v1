"""
Entry point for the advanced modular voice assistant.
"""
from src.config import Settings
from src.assistant import PersonalAI

def main() -> None:
    cfg = Settings.load()
    assistant = PersonalAI(cfg)
    assistant.run()

if __name__ == "__main__":
    main()
