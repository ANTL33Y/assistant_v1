import requests
from src.plugins.base import AssistantPlugin


class NewsPlugin(AssistantPlugin):
    """Fetch latest news headlines."""

    name = "News"
    description = "Get recent news headlines from NewsAPI"

    def setup(self, assistant) -> None:
        self.api_key = getattr(assistant.cfg, "news_api_key", "")
        self.session = requests.Session()

    def register(self):
        return {"news": self.handle_news}

    def handle_news(self, command: str, *args, **kwargs):
        if not self.api_key:
            return "News API key is not configured."
        try:
            resp = self.session.get(
                "https://newsapi.org/v2/top-headlines",
                params={"country": "us", "pageSize": 3, "apiKey": self.api_key},
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
            articles = data.get("articles") or []
            if not articles:
                return "I couldn't find any news right now."
            headlines = [a.get("title", "") for a in articles if a.get("title")]
            return "Here are the latest headlines: " + "; ".join(headlines)
        except Exception as exc:
            return f"Failed to fetch news: {exc}"
