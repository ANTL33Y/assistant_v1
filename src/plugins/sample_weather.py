from src.plugins.base import AssistantPlugin

class WeatherPlugin(AssistantPlugin):
    name = "Weather"
    description = "Provides weather information."

    def register(self):
        return {"weather": self.handle_weather}

    def handle_weather(self, command: str, *args, **kwargs):
        # In production, integrate with a real weather API here
        return "The weather is sunny and 25°C. (Sample plugin response)" 