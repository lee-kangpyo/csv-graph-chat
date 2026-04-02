import os
from openai import OpenAI


class LLMClient:
    _instance = None

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("Z_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

        self.client = OpenAI(api_key=api_key, base_url=base_url, max_retries=5)
        self.model = os.getenv("LLM_MODEL", "gpt-4o")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def chat(self, messages: list[dict], stream: bool = False):
        return self.client.chat.completions.create(
            model=self.model, messages=messages, stream=stream
        )
