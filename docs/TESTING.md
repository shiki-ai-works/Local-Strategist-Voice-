# Testing Guide

## 1. リポジトリを取得

```powershell
git clone https://github.com/shiki-ai-works/Local-Strategist-Voice-.git
cd Local-Strategist-Voice-
```

## 2. Python仮想環境を作る

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 3. 設定ファイルを作る

```powershell
Copy-Item config.example.json config.json
```

必要なら `config.json` を開いて、以下を変更します。

- `llm.base_url`: LM Studio のURL
- `llm.model`: LM Studioで読み込んでいるモデル名
- `speech.base_url`: AivisSpeech / VOICEVOX互換APIのURL
- `speech.speaker`: 話者ID

## 4. 外部アプリを起動

### LM Studio

1. モデルを読み込む
2. Local Server を開く
3. OpenAI Compatible Server を起動する

想定URL:

```text
http://localhost:1234/v1
```

### AivisSpeech / VOICEVOX互換API

音声合成APIを起動します。

想定URL:

```text
http://localhost:10101
```

## 5. アプリを起動

```powershell
python -m local_strategist_voice
```

## 6. 動作確認

入力欄に以下を入れて送信します。

```text
今日の開発方針を短く整理して。
```

期待する結果:

- 画面にUserの発言が出る
- LLMから返答が出る
- 音声が再生される
- `logs/YYYY-MM-DD.md` が作成される

## よくあるエラー

### config.json が見つかりません

`config.example.json` を `config.json` にコピーしてください。

### Connection refused / 接続できません

LM Studio または AivisSpeech のAPIが起動していません。

### 返答は出るが音声が出ない

AivisSpeech / VOICEVOX互換APIのURLまたは話者IDが違う可能性があります。

### モデルが見つからない

`config.json` の `llm.model` を、LM Studioで実際に読み込んでいるモデル名に合わせてください。
