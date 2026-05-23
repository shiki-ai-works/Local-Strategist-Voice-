from __future__ import annotations

import requests

from .config import LLMConfig


class LLMClient:
    def __init__(self, config: LLMConfig, system_prompt: str) -> None:
        self.config = config
        self.system_prompt = system_prompt
        self.history: list[dict[str, str]] = []

    def chat(self, user_text: str) -> str:
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.history[-12:])
        messages.append({"role": "user", "content": user_text})

        response = requests.post(
            f"{self.config.base_url}/chat/completions",
            json={
                "model": self.config.model,
                "messages": messages,
                "temperature": self.config.temperature,
                "max_tokens": self.config.max_tokens,
            },
            timeout=120,
        )
        response.raise_for_status()
        data = response.json()
        assistant_text = data["choices"][0]["message"]["content"].strip()

        self.history.append({"role": "user", "content": user_text})
        self.history.append({"role": "assistant", "content": assistant_text})
        return assistant_text
