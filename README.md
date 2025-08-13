# discordbot-yomiage

Discord上でテキストを読み上げる、簡易的なBotです。  
[VOICEVOX](https://voicevox.hiroshiba.jp/)のAPIを使用して、音声を生成・VCで再生します。

apiには僕が提供している https://voicevox.moyashi.xyz を利用しています

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

これで設定は完了です

### 実行
```bash
python3 main.py
```
