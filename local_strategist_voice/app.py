from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QVBoxLayout,
    QWidget,
)

from .config import load_config, load_persona
from .llm_client import LLMClient
from .logger import MarkdownLogger
from .speech_client import SpeechClient


class ChatWorker(QObject):
    finished = Signal(str)
    failed = Signal(str)

    def __init__(self, llm: LLMClient, speech: SpeechClient, logger: MarkdownLogger, user_text: str) -> None:
        super().__init__()
        self.llm = llm
        self.speech = speech
        self.logger = logger
        self.user_text = user_text

    def run(self) -> None:
        try:
            assistant_text = self.llm.chat(self.user_text)
            self.logger.append_exchange(self.user_text, assistant_text)
            wav_bytes = self.speech.synthesize(assistant_text)
            self.speech.play_wav_bytes(wav_bytes)
            self.finished.emit(assistant_text)
        except Exception as exc:  # noqa: BLE001
            self.failed.emit(str(exc))


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Local Strategist Voice / 音声参謀")
        self.resize(900, 700)

        self.config = load_config()
        persona = load_persona(self.config.app.persona_file)
        self.llm = LLMClient(self.config.llm, persona)
        self.speech = SpeechClient(self.config.speech)
        self.logger = MarkdownLogger(self.config.app.log_dir)
        self.worker_thread: QThread | None = None

        self.status_label = QLabel("準備完了")
        self.chat_view = QPlainTextEdit()
        self.chat_view.setReadOnly(True)
        self.input_box = QPlainTextEdit()
        self.input_box.setPlaceholderText("相談したいことを入力してください。")
        self.input_box.setFixedHeight(120)

        self.send_button = QPushButton("送信して話す")
        self.send_button.clicked.connect(self.on_send)

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.send_button)

        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.chat_view)
        layout.addWidget(self.input_box)
        layout.addLayout(bottom_layout)

        root = QWidget()
        root.setLayout(layout)
        self.setCentralWidget(root)

    def on_send(self) -> None:
        user_text = self.input_box.toPlainText().strip()
        if not user_text:
            return

        self.input_box.clear()
        self.chat_view.appendPlainText(f"User:\n{user_text}\n")
        self.status_label.setText("考えています……")
        self.send_button.setEnabled(False)

        self.worker_thread = QThread()
        self.worker = ChatWorker(self.llm, self.speech, self.logger, user_text)
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_worker_finished)
        self.worker.failed.connect(self.on_worker_failed)
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.failed.connect(self.worker_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.failed.connect(self.worker.deleteLater)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)
        self.worker_thread.start()

    def on_worker_finished(self, assistant_text: str) -> None:
        self.chat_view.appendPlainText(f"Assistant:\n{assistant_text}\n")
        self.status_label.setText("準備完了")
        self.send_button.setEnabled(True)

    def on_worker_failed(self, message: str) -> None:
        self.status_label.setText("エラー")
        self.send_button.setEnabled(True)
        QMessageBox.critical(self, "エラー", message)


def main() -> None:
    app = QApplication([])
    try:
        window = MainWindow()
    except Exception as exc:  # noqa: BLE001
        QMessageBox.critical(None, "起動エラー", str(exc))
        raise
    window.show()
    app.exec()
