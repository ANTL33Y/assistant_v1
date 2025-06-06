class TextVoiceIO:
    """Simplified voice I/O that captures responses as text."""
    def __init__(self, settings=None) -> None:
        self.cfg = settings
        self.last_output = ""

    def speak(self, text: str) -> None:
        """Store spoken text for retrieval by the GUI."""
        self.last_output = text

    def listen(self) -> str:  # pragma: no cover - not used
        return ""
