from typing import Any, Dict, Callable

class AssistantPlugin:
    """
    Base class for all assistant plugins.
    Plugins should inherit from this and implement the register and handle methods.
    """
    name: str = "BasePlugin"
    description: str = "Base plugin class."

    def register(self) -> Dict[str, Callable[[str, Any], Any]]:
        """
        Return a dict mapping command names to handler functions.
        Returns:
            Dict[str, Callable]: Mapping of command names to handler functions.
        Example: {"weather": self.handle_weather}
        """
        return {}

    def handle(self, command: str, *args: Any, **kwargs: Any) -> Any:
        """
        Handle a command. Should be overridden by plugin implementations.
        Args:
            command (str): The command string.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            Any: The result of the command handling.
        Raises:
            NotImplementedError: If not implemented in subclass.
        """
        raise NotImplementedError 