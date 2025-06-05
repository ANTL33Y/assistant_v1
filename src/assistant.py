import logging
import datetime as dt
import os
import subprocess
import webbrowser
import json
from typing import Any
from src.config import Settings
from src.memory import Memory
from src.voice import VoiceIO
from src.llm import LLMClient
from src.semantic import SemanticMemory

try:
    from duckduckgo_search import DDGS
except ImportError:
    DDGS = None

class PersonalAI:
    def __init__(self, cfg: Settings = Settings()):
        self.cfg = cfg
        self.memory = Memory(cfg.memory_path, cfg.max_interactions)
        self.voice = VoiceIO(cfg)
        self.llm = LLMClient(cfg, self.memory)
        self.semantic = SemanticMemory(self.memory, cfg)
        logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
        logging.info("Assistant ready – say a wake word to begin.")

    def _get_current_time(self) -> str:
        return dt.datetime.now().strftime("%I:%M %p")

    def _get_current_date(self) -> str:
        return dt.datetime.now().strftime("%A, %B %d, %Y")

    def _open_application(self, app_name: str) -> str:
        try:
            app_name_lower = app_name.lower()
            if "notepad" in app_name_lower:
                self._system_action("notepad")
                return f"Opening {app_name}."
            elif "calculator" in app_name_lower:
                self._system_action("calculator")
                return f"Opening {app_name}."
            elif "browser" in app_name_lower or "chrome" in app_name_lower:
                self._system_action("browser")
                return f"Opening {app_name}."
            else:
                return f"Sorry, I don't know how to open '{app_name}'. Application not recognized."
        except Exception as e:
            logging.error(f"Error opening application {app_name}: {e}")
            return f"Sorry, I encountered an error trying to open {app_name}."

    def _remember_user_name(self, name: str) -> str:
        try:
            if not name or not isinstance(name, str) or len(name.strip()) == 0:
                return "Please provide a valid name to remember."
            self.memory.data["user_preferences"]["name"] = name.strip()
            self.memory.save()
            return f"Okay, I'll remember your name is {name.strip()}."
        except Exception as e:
            logging.error(f"Error remembering user name '{name}': {e}")
            return "Sorry, I had trouble remembering that name."

    def _recall_user_name(self) -> str:
        name = self.memory.data.get("user_preferences", {}).get("name")
        if name:
            return f"Your name is {name}."
        return "I don't believe I know your name yet."

    def _remember_fact(self, fact: str) -> str:
        try:
            if not fact or not isinstance(fact, str) or len(fact.strip()) == 0:
                return "Please provide a valid fact to remember."
            fact_text = fact.strip()
            fact_id = dt.datetime.now().isoformat()
            fact_embedding = self.semantic.embed_fact(fact_text)
            self.memory.data.setdefault("learned_facts", {})[fact_id] = {
                "text": fact_text,
                "timestamp": fact_id,
                "embedding": fact_embedding
            }
            self.memory.save()
            return f"Okay, I've remembered that: {fact_text}"
        except Exception as e:
            logging.error(f"Error remembering fact '{fact}': {e}")
            return "Sorry, I had trouble remembering that fact."

    def _recall_facts(self, topic: str | None = None) -> str:
        return self.semantic.recall_facts(topic)

    def _lock_computer(self) -> str:
        try:
            self._system_action("lock")
            return "Locking the computer now."
        except Exception as e:
            logging.error(f"Error locking computer: {e}")
            return "Sorry, I encountered an error trying to lock the computer."

    def _search_web(self, query: str) -> str:
        if not DDGS:
            return "Web search functionality is not available. The DDGS library is missing."
        if not query or not isinstance(query, str) or len(query.strip()) == 0:
            return "Please provide a valid search query."
        try:
            logging.info(f"Performing web search for: {query}")
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=3))
            if not results:
                return f"I couldn't find any web results for '{query}'."
            snippets = [f"{r['title']}: {r['body']}" for r in results]
            return "Here's what I found on the web:\n" + "\n\n".join(snippets)
        except Exception as e:
            logging.error(f"Error during web search for '{query}': {e}")
            return f"Sorry, I encountered an error while searching the web for '{query}'."

    def _system_action(self, key: str) -> None:
        if key == "notepad":
            subprocess.Popen(["notepad.exe"])
        elif key == "calculator":
            subprocess.Popen(["calc.exe"])
        elif key == "browser":
            webbrowser.open("https://www.google.com")
        elif key == "lock":
            os.system("rundll32.exe user32.dll,LockWorkStation")

    def _process(self, cmd: str) -> bool:
        self.memory.append("user_command", cmd, cmd)
        if not self.llm.openai_client:
            self.voice.speak("My advanced thinking capabilities are offline. Please configure the OpenAI API key.")
            if any(w in cmd for w in ("quit", "exit", "goodbye", "stop")):
                self.voice.speak("Goodbye!")
                return False
            self.voice.speak("Sorry, I can't process that without my core intelligence.")
            return True
        # Prepare conversation history for context
        history = self.memory.data.get("interactions", [])
        user_name = self.memory.data.get("user_preferences", {}).get("name", "")
        system_prompt = (
            "You are a helpful and concise voice assistant. "
            f"{f'The user you are talking to is named {user_name}. ' if user_name else ''}"
            "Use the available tools to answer questions, perform actions, or remember information. "
            "When a tool provides information or an outcome (success or error), incorporate it naturally into your response to the user. "
            "If a tool reports an error, inform the user clearly about the problem. "
            "If the user asks to quit or says goodbye, respond conversationally and prepare to terminate. "
            "Keep your spoken responses brief and natural for a voice interface."
        )
        messages = [{"role": "system", "content": system_prompt}]
        for interaction in history[-5:]:
            if interaction["type"] == "user_command":
                messages.append({"role": "user", "content": interaction["content"]})
            elif interaction["type"] == "ai_response":
                if interaction.get("content"):
                    messages.append({"role": "assistant", "content": interaction["content"]})
        messages.append({"role": "user", "content": cmd})
        tools = [
            {"type": "function", "function": {"name": "get_current_time", "description": "Get the current time."}},
            {"type": "function", "function": {"name": "get_current_date", "description": "Get the current date."}},
            {"type": "function", "function": {"name": "open_application", "description": "Opens a specified application like notepad, calculator, or browser.", "parameters": {"type": "object", "properties": {"app_name": {"type": "string", "description": "The name of the application to open (e.g., 'notepad', 'calculator', 'browser')."}}, "required": ["app_name"]}}},
            {"type": "function", "function": {"name": "remember_user_name", "description": "Remembers the user's name.", "parameters": {"type": "object", "properties": {"name": {"type": "string", "description": "The user's name."}}, "required": ["name"]}}},
            {"type": "function", "function": {"name": "recall_user_name", "description": "Recalls the user's name if it has been previously remembered."}},
            {"type": "function", "function": {"name": "remember_fact", "description": "Stores a specific piece of information or fact provided by the user for later recall. Example: 'Remember that my anniversary is on June 5th.'", "parameters": {"type": "object", "properties": {"fact": {"type": "string", "description": "The fact or piece of information to remember."}}, "required": ["fact"]}}},
            {"type": "function", "function": {"name": "recall_facts", "description": "Recalls previously remembered facts. Can optionally filter by a topic if the user specifies one. Example: 'What do you remember about my car?'", "parameters": {"type": "object", "properties": {"topic": {"type": "string", "description": "An optional topic to filter recalled facts."}}}}},
            {"type": "function", "function": {"name": "lock_computer", "description": "Locks the computer workstation."}},
            {"type": "function", "function": {"name": "search_web", "description": "Searches the web for information on a given query and provides a summary or top results. Use this for real-time information, current events, or topics not covered by other tools.", "parameters": {"type": "object", "properties": {"query": {"type": "string", "description": "The search query."}}, "required": ["query"]}}}
        ]
        available_functions = {
            "get_current_time": self._get_current_time,
            "get_current_date": self._get_current_date,
            "open_application": self._open_application,
            "remember_user_name": self._remember_user_name,
            "recall_user_name": self._recall_user_name,
            "remember_fact": self._remember_fact,
            "recall_facts": self._recall_facts,
            "lock_computer": self._lock_computer,
            "search_web": self._search_web,
        }
        try:
            llm_response = self.llm.openai_client.chat.completions.create(
                model=self.cfg.openai_model_name,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                temperature=0.7,
                max_tokens=150
            )
            response_message = llm_response.choices[0].message
            tool_calls = response_message.tool_calls
            if tool_calls:
                self.memory.append("ai_tool_decision", f"Decided to call tools: {[tc.function.name for tc in tool_calls]}", cmd)
                messages.append(response_message)
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_to_call = available_functions[function_name]
                    function_args = json.loads(tool_call.function.arguments)
                    self.memory.append("tool_call", f"Calling: {function_name} with args: {function_args}", cmd)
                    function_response = function_to_call(**function_args)
                    self.memory.append("tool_response", f"Function {function_name} returned: {function_response}", cmd)
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    })
                second_response = self.llm.openai_client.chat.completions.create(
                    model=self.cfg.openai_model_name,
                    messages=messages,
                )
                ai_text_response = second_response.choices[0].message.content.strip()
            else:
                ai_text_response = response_message.content.strip() if response_message.content else "I'm not sure how to respond to that."
            if any(w in cmd.lower() for w in ("quit", "exit", "stop")) or "goodbye" in ai_text_response.lower():
                final_goodbye = ai_text_response or f"Goodbye{', ' + user_name if user_name else ''}!"
                self.voice.speak(final_goodbye)
                self.memory.append("session_end", final_goodbye)
                return False
            self.voice.speak(ai_text_response)
            self.memory.append("ai_response", ai_text_response)
            return True
        except Exception as e:
            logging.error(f"LLM processing error: {e}")
            self.voice.speak("I seem to have trouble thinking right now. Please try again.")
            return True

    def run(self) -> None:
        self.voice.speak("Personal AI online.")
        while True:
            heard = self.voice.listen()
            if not heard:
                continue
            if any(wake in heard for wake in self.cfg.wake_words):
                name = self.memory.data["user_preferences"].get("name", "")
                self.voice.speak(f"Yes{', ' + name if name else ''}?")
                heard = self.voice.listen()
            if not heard:
                continue
            if not self._process(heard):
                break 