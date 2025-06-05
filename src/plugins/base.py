from typing import Any, Dict, Callable

class AssistantPlugin:
    """
    Base class for all assistant plugins.
    Plugins should inherit from this and implement the register and handle methods.
    """
    name: str = "BasePlugin"
    description: str = "Base plugin class."

    def register(self) -> Dict[str, Callable]:
        """
        Return a dict mapping command names to handler functions.
        Example: {"weather": self.handle_weather}
        """
        return {}

    def handle(self, command: str, *args, **kwargs) -> Any:
        """
        Handle a command. Should be overridden by plugin implementations.
        """
        raise NotImplementedError 