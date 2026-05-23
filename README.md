# Local Strategist Voice / 音声参謀

Local Strategist Voice は、ローカルLLMと音声合成エンジンをつなぎ、ChatGPTのように作戦会議できるデスクトップアプリです。

初期版では、常駐監視や画面監視は入れません。まずは安全で小さく動く MVP として、以下を実装対象にします。

- LM Studio などの OpenAI 互換ローカルLLM API と接続
- AivisSpeech / VOICEVOX 互換 API と接続
- Python + PySide6 のデスクトップUI
- テキスト入力による対話
- 応答の音声再生
- Markdownログ保存
- `persona.md` による人格・口調設定
- `config.json` による接続先・モデル・話者設定

## セットアップ

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy config.example.json config.json
python -m local_strategist_voice
```

PowerShell の場合:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item config.example.json config.json
python -m local_strategist_voice
```

## 必要な外部アプリ

### 1. LM Studio

LM Studio 側で Local Server を起動し、OpenAI compatible endpoint を有効にしてください。

標準想定:

```text
http://localhost:1234/v1/chat/completions
```

### 2. AivisSpeech / VOICEVOX 互換API

音声合成APIを起動してください。

標準想定:

```text
http://localhost:10101
```

AivisSpeech が VOICEVOX 互換APIとして動作している前提です。

## 現在の開発方針

1. まずテキスト入力 → LLM応答 → 音声再生を完成させる
2. ログ保存を安定させる
3. persona.md を読み込んでキャラクター性を固定する
4. その後、マイク入力や画面監視を追加する

## MVPの範囲外

- 常時画面監視
- マイク常時待ち受け
- PC操作の自動実行
- 長期記憶RAG
- 配布用インストーラー

これらは後続フェーズで扱います。
