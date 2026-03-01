# main.py
import os
import re
import sys
import discord
from discord.ext import commands
from dotenv import load_dotenv

# .env からトークン読込
load_dotenv()
token = (
    os.getenv("TOKEN")
    or os.getenv("BOT_TOKEN")
    or os.getenv("DISCORD_TOKEN")
)

# Bot初期化
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Cogs を読み込む
async def load_cogs():
    cogs_dir = "./Cogs"

    names = []
    try:
        for filename in os.listdir(cogs_dir):
            if not filename.endswith(".py"):
                continue
            if filename.startswith("_"):
                continue
            if not re.fullmatch(r"[A-Za-z_]\w+\.py", filename):
                continue
            names.append(filename[:-3])
    except FileNotFoundError:
        os.makedirs(cogs_dir, exist_ok=True)

    priority = ["vending", "paypay"]
    ordered = [n for n in priority if n in names] + [n for n in names if n not in priority]

    for name in ordered:
        mod = f"Cogs.{name}"
        try:
            await bot.load_extension(mod)
            print(f"[COG] Loaded: {mod}")
        except commands.errors.ExtensionAlreadyLoaded:
            print(f"[COG] Already loaded: {mod}")
        except Exception as e:
            print(f"[COG] Failed to load {mod}: {e}")

    try:
        synced = await bot.tree.sync()
        print(f"[SLASH] Synced: {len(synced)}")
    except Exception as e:
        print(f"[SLASH] Sync failed: {e}")

bot.setup_hook = load_cogs

@bot.event
async def on_ready():
    print("Bot Is Ready.")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="🍞サーバー"
        ),
        status=discord.Status.online
    )

if not token:
    print("環境変数 TOKEN/BOT_TOKEN/DISCORD_TOKEN を設定してください。", file=sys.stderr)
    sys.exit(1)

bot.run(token)
