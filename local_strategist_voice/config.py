from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class LLMConfig:
    base_url: str
    model: str
    temperature: float
    max_tokens: int


@dataclass(frozen=True)
class SpeechConfig:
    base_url: str
    speaker: int
    speed_scale: float
    pitch_scale: float
    intonation_scale: float
    volume_scale: float


@dataclass(frozen=True)
class AppConfig:
    log_dir: Path
    persona_file: Path


@dataclass(frozen=True)
class Config:
    llm: LLMConfig
    speech: SpeechConfig
    app: AppConfig


def load_config(path: str | Path = "config.json") -> Config:
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(
            "config.json が見つかりません。config.example.json を config.json にコピーしてください。"
        )

    data = json.loads(config_path.read_text(encoding="utf-8"))
    return _parse_config(data)


def _parse_config(data: dict[str, Any]) -> Config:
    llm = data.get("llm", {})
    speech = data.get("speech", {})
    app = data.get("app", {})

    return Config(
        llm=LLMConfig(
            base_url=str(llm.get("base_url", "http://localhost:1234/v1")).rstrip("/"),
            model=str(llm.get("model", "local-model")),
            temperature=float(llm.get("temperature", 0.7)),
            max_tokens=int(llm.get("max_tokens", 800)),
        ),
        speech=SpeechConfig(
            base_url=str(speech.get("base_url", "http://localhost:10101")).rstrip("/"),
            speaker=int(speech.get("speaker", 888753760)),
            speed_scale=float(speech.get("speed_scale", 1.0)),
            pitch_scale=float(speech.get("pitch_scale", 0.0)),
            intonation_scale=float(speech.get("intonation_scale", 1.0)),
            volume_scale=float(speech.get("volume_scale", 1.0)),
        ),
        app=AppConfig(
            log_dir=Path(app.get("log_dir", "logs")),
            persona_file=Path(app.get("persona_file", "persona.md")),
        ),
    )


def load_persona(path: str | Path) -> str:
    persona_path = Path(path)
    if not persona_path.exists():
        return "君は実務的で頼れる音声参謀として、簡潔に日本語で答える。"
    return persona_path.read_text(encoding="utf-8").strip()
