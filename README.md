# discordbot-yomiage

Discord上でテキストを読み上げる、簡易的なBotです

[VOICEVOX](https://voicevox.hiroshiba.jp/)のEngineを使用して、音声を生成・VCで再生します

APIには僕が提供している https://voicevox.moyashi.xyz を利用しています
> [!CAUTION]
> APIを悪用して負荷をかける行為や攻撃行為は禁止します
> そのようなこ行為が確認された場合は永久的なIPBANを行います

---

## 🔧 インストール

### 必要なライブラリのインストール

```bash
pip install -U discord.py aiohttp
```
### TOKENのセット
```python
TOKEN = "DiscordBotToken"
```

### 実行
```bash
python3 main.py
```

### 設定変更方法
```python
VOICEVOX_URL, VOICE_ID, SPAM_INTERVAL = "https://voicevox.moyashi.xyz", 1, 10
```
VOICEVOX_URLはVOICEVOX engineを動作させているURL

VOICE_IDは話者IDです(この数値をいじることで話者を変更できます)

SPAM_INTERVALは〇秒間で同じ内容3回までと設定するものです
- 5 とした場合は5秒間で同じ内容3回まで、それ以上は無視する

