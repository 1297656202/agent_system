# agents/base.py
from abc import ABC, abstractmethod
from typing import Any

from llm_client import LLMClient


class BaseAgent(ABC):
    """
    Abstract base class for all agents.
    """

    def __init__(self, name: str, system_prompt: str, llm_client: LLMClient):
        self.name = name
        self.system_prompt = system_prompt
        # print("Initializing BaseAgent with system prompt:", system_prompt)
        self.llm = llm_client

    @abstractmethod
    def run(self, *args, **kwargs) -> Any:
        """
        Main entry for the agent.
        """
        raise NotImplementedError

    def _chat(self, user_content: str) -> str:
        """
        Helper to call LLM with a single user message.
        """
        messages = [{"role": "user", "content": user_content}]
        return self.llm.chat(self.system_prompt, messages)

