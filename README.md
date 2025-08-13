# discordbot-yomiage

Discord上でテキストを読み上げる、簡易的なBotです。  
[VOICEVOX](https://voicevox.hiroshiba.jp/)のAPIを使用して、音声を生成・VCで再生します。

APIには僕が提供している https://voicevox.moyashi.xyz を利用しています

APIを悪用して負荷をかける行為や攻撃行為は禁止します
確認した場合は永久的なIPBANを行います

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
