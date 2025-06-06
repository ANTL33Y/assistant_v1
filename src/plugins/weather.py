from __future__ import annotations
import re
import requests
from src.plugins.base import AssistantPlugin

class WeatherPlugin(AssistantPlugin):
    """Fetch current weather information using OpenWeatherMap."""

    name = "Weather"
    description = "Provides up-to-date weather information for a location."

    def setup(self, assistant) -> None:
        self.api_key = getattr(assistant.cfg, "weather_api_key", "")
        self.default_location = getattr(assistant.cfg, "default_location", "New York")
        self.session = requests.Session()

    def register(self):
        return {"weather": self.handle_weather}

    def _extract_location(self, command: str) -> str:
        match = re.search(r"weather(?: in| for| at)? ([\w\s]+)", command, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return self.default_location

    def handle_weather(self, command: str, *args, **kwargs):
        if not self.api_key:
            return "Weather API key is not configured."

        location = self._extract_location(command)
        try:
            resp = self.session.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={"q": location, "appid": self.api_key, "units": "metric"},
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            city = data.get("name", location)
            return f"The weather in {city} is {desc} with a temperature of {temp}\u00b0C."
        except requests.HTTPError:
            return f"I couldn't get the weather for {location}."
        except Exception as exc:
            return f"An error occurred fetching the weather: {exc}"
