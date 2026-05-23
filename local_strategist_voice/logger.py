from __future__ import annotations

from datetime import datetime
from pathlib import Path


class MarkdownLogger:
    def __init__(self, log_dir: Path) -> None:
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        date = datetime.now().strftime("%Y-%m-%d")
        self.path = self.log_dir / f"{date}.md"

    def append_exchange(self, user_text: str, assistant_text: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = (
            f"\n## {timestamp}\n\n"
            f"### User\n\n{user_text.strip()}\n\n"
            f"### Assistant\n\n{assistant_text.strip()}\n"
        )
        with self.path.open("a", encoding="utf-8") as file:
            file.write(entry)
