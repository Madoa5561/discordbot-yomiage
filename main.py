import discord, aiohttp, asyncio, os, tempfile, time
from discord import app_commands
from collections import defaultdict, deque

TOKEN = "discordBotToken"
VOICEVOX_URL, VOICE_ID, SPAM_INTERVAL = "https://voicevox.moyashi.xyz", 1, 10
MSG_HIST, MSG_TIME = defaultdict(lambda: deque(maxlen=3)), defaultdict(lambda: deque(maxlen=3))

intents = discord.Intents.default()
intents.message_content = intents.voice_states = intents.guilds = True

class Bot(discord.Client):
    def __init__(self): super().__init__(intents=intents); self.tree = app_commands.CommandTree(self); self.vc = {}
    async def setup_hook(self): await self.tree.sync()
bot = Bot()

async def synth(text, speaker=VOICE_ID):
    async with aiohttp.ClientSession() as s:
        async with s.post(f"{VOICEVOX_URL}/audio_query", params={"text": text, "speaker": speaker}) as r: q = await r.json()
        async with s.post(f"{VOICEVOX_URL}/synthesis", params={"speaker": speaker}, json=q) as r: return await r.read()

async def play(vc, text):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f: f.write(await synth(text)); n = f.name
    src = discord.FFmpegPCMAudio(n)
    if not vc.is_playing(): vc.play(src);  [await asyncio.sleep(0.5) for _ in iter(lambda: vc.is_playing(), False)]
    os.remove(n)

def emb(t, d, c=discord.Color.blue()): e = discord.Embed(title=t, description=d, color=c); e.set_footer(text="Voicevox Bot"); return e

@bot.tree.command(name="connect", description="VCに接続します")
async def connect(i: discord.Interaction):
    if not i.guild: return await i.response.send_message(embed=emb("エラー", "サーバー内でのみ使用できます。", discord.Color.red()), ephemeral=True)
    m = i.guild.get_member(i.user.id)
    if not m or not m.voice or not m.voice.channel: return await i.response.send_message(embed=emb("エラー", "VCに参加してから実行してください。", discord.Color.red()), ephemeral=True)
    if i.guild.id in bot.vc: return await i.response.send_message(embed=emb("情報", "既に接続しています。", discord.Color.orange()), ephemeral=True)
    vc = await m.voice.channel.connect(); bot.vc[i.guild.id] = vc
    await i.response.send_message(embed=emb("接続", "VCに接続しました。", discord.Color.green()))
    try: await play(vc, "接続しました。")
    except: pass

@bot.tree.command(name="disconnect", description="VCから切断します")
async def disconnect(i: discord.Interaction):
    if not i.guild: return await i.response.send_message(embed=emb("エラー", "サーバー内でのみ使用できます。", discord.Color.red()), ephemeral=True)
    vc = bot.vc.pop(i.guild.id, None)
    if vc: await vc.disconnect(); await i.response.send_message(embed=emb("切断", "VCから切断しました。", discord.Color.green()))
    else: await i.response.send_message(embed=emb("情報", "未接続です。", discord.Color.orange()), ephemeral=True)

@bot.event
async def on_message(m):
    if m.author.bot or not m.guild: return
    uid, c, now = m.author.id, m.content.strip(), time.time()
    h, t = MSG_HIST[uid], MSG_TIME[uid]
    if len(h) == 3 and all(msg == c for msg in h) and now - t[0] < SPAM_INTERVAL: return
    h.append(c); t.append(now)
    vc = bot.vc.get(m.guild.id)
    if vc and vc.is_connected():
        try: await play(vc, f"{m.author.display_name}、{m.content}")
        except: pass

bot.run(TOKEN)
