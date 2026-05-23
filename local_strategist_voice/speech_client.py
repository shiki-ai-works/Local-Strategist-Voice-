from __future__ import annotations

import tempfile
import wave
from pathlib import Path

import requests

from .config import SpeechConfig


class SpeechClient:
    def __init__(self, config: SpeechConfig) -> None:
        self.config = config

    def synthesize(self, text: str) -> bytes:
        query_response = requests.post(
            f"{self.config.base_url}/audio_query",
            params={"text": text, "speaker": self.config.speaker},
            timeout=30,
        )
        query_response.raise_for_status()
        query = query_response.json()
        query["speedScale"] = self.config.speed_scale
        query["pitchScale"] = self.config.pitch_scale
        query["intonationScale"] = self.config.intonation_scale
        query["volumeScale"] = self.config.volume_scale

        synthesis_response = requests.post(
            f"{self.config.base_url}/synthesis",
            params={"speaker": self.config.speaker},
            json=query,
            timeout=120,
        )
        synthesis_response.raise_for_status()
        return synthesis_response.content

    def save_wav(self, wav_bytes: bytes, path: str | Path) -> Path:
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(wav_bytes)
        return output_path

    def play_wav_bytes(self, wav_bytes: bytes) -> None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_file.write(wav_bytes)
            temp_path = Path(temp_file.name)
        play_wav_file(temp_path)


def play_wav_file(path: Path) -> None:
    try:
        import winsound

        winsound.PlaySound(str(path), winsound.SND_FILENAME)
        return
    except ImportError:
        pass

    # macOS / Linux の最低限フォールバック。再生できない環境では保存だけ行う。
    _validate_wav(path)


def _validate_wav(path: Path) -> None:
    with wave.open(str(path), "rb") as wav_file:
        wav_file.getparams()
