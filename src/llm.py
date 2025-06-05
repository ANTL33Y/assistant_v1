from src.logging import get_logger
from typing import Any, Tuple

try:
    import openai
except ImportError:
    openai = None


class LLMClient:
    """
    Handles interaction with the language model (LLM) provider (e.g., OpenAI).
    """
    def __init__(self, settings: Any, memory: Any) -> None:
        """
        Initialize the LLM client.
        Args:
            settings: The configuration/settings object.
            memory: The memory object for persistent storage.
        """
        self.cfg = settings
        self.memory = memory
        self.openai_client = None
        self.logger = get_logger(__name__)
        if self.cfg.openai_api_key and openai:
            self.openai_client = openai.OpenAI(api_key=self.cfg.openai_api_key)
            self.logger.info("OpenAI client initialized.")

    def process(self, cmd: str) -> Tuple[str, bool]:
        """
        Process a user command using the LLM.
        Args:
            cmd (str): The user command.
        Returns:
            Tuple[str, bool]: (response, continue_flag)
        """
        self.memory.append("user_command", cmd, cmd)
        if not self.openai_client:
            return (
                "My advanced thinking capabilities are offline. "
                "Please configure the OpenAI API key.",
                True,
            )
        history = self.memory.data.get("interactions", [])
        user_name = self.memory.data.get("user_preferences", {}).get("name", "")
        system_prompt = (
            "You are a helpful and concise voice assistant. "
            f"{f'The user you are talking to is named {user_name}. ' if user_name else ''}"
            "Use the available tools to answer questions, perform actions, or "
            "remember information. "
            "When a tool provides information or an outcome (success or error), "
            "incorporate it naturally into your response to the user. "
            "If a tool reports an error, inform the user clearly about the problem. "
            "If the user asks to quit or says goodbye, respond conversationally and "
            "prepare to terminate. "
            "Keep your spoken responses brief and natural for a voice interface."
        )
        messages = [{"role": "system", "content": system_prompt}]
        for interaction in history[-5:]:
            if interaction["type"] == "user_command":
                messages.append({
                    "role": "user",
                    "content": interaction["content"],
                })
            elif interaction["type"] == "ai_response":
                if interaction.get("content"):
                    messages.append({
                        "role": "assistant",
                        "content": interaction["content"],
                    })
        messages.append({"role": "user", "content": cmd})
        # Tool/function definitions will be injected by the assistant class
        return (
            "[LLMClient: Tool/function logic to be injected by assistant class]",
            True,
        ) 