import io
from src.logging import get_logger
import requests
import pygame
import speech_recognition as sr

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None


class VoiceIO:
    def __init__(self, settings):
        self.cfg = settings
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        pygame.mixer.init()
        self.logger = get_logger(__name__)

    def speak(self, text: str) -> None:
        self.logger.info("AI: %s", text)
        if self.cfg.api_key:
            try:
                resp = requests.post(
                    self.cfg.tts_url,
                    json={
                        "text": text,
                        "model_id": "eleven_monolingual_v1",
                        "voice_settings": {
                            "stability": 0.5,
                            "similarity_boost": 0.75,
                        },
                    },
                    headers={
                        "Accept": "audio/mpeg",
                        "Content-Type": "application/json",
                        "xi-api-key": self.cfg.api_key,
                    },
                    timeout=20,
                )
                resp.raise_for_status()
                pygame.mixer.music.load(io.BytesIO(resp.content))
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(120)
                return
            except Exception as exc:
                self.logger.warning(
                    "ElevenLabs TTS failed: %s – using offline engine", exc
                )
        if pyttsx3:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        else:
            self.logger.warning("No TTS engine available. Text will not be spoken.")

    def listen(self) -> str:
        with self.microphone as src:
            self.recognizer.adjust_for_ambient_noise(
                src, duration=self.cfg.ambient_adjust_sec
            )
            try:
                audio = self.recognizer.listen(
                    src,
                    timeout=self.cfg.listen_timeout,
                    phrase_time_limit=self.cfg.phrase_time_limit,
                )
                return self.recognizer.recognize_google(audio).lower()
            except (sr.WaitTimeoutError, sr.UnknownValueError):
                return ""
            except sr.RequestError as err:
                self.logger.error("Speech recognition error: %s", err)
                return "" 