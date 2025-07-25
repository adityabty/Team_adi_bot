from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputStream, AudioPiped
from yt_dlp import YoutubeDL
import os

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client("music-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
vc = PyTgCalls(app)

ydl_opts = {"format": "bestaudio"}

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_text(
        f"👋 Hello {message.from_user.mention}!\n\n🎵 Welcome to VC Music Bot.\n\n🧑‍💻 Developer: @adidevloper",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🎧 Join VC", callback_data="join")],
            [InlineKeyboardButton("🧑‍💻 Founder", url="https://t.me/adidevloper")]
        ])
    )

@app.on_message(filters.command("play") & filters.group)
async def play(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("❗ Usage: `/play song name or YouTube URL`")
    query = " ".join(message.command[1:])

    msg = await message.reply("🔍 Searching...")
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        url = info["url"]
        title = info.get("title")

    chat_id = message.chat.id
    await vc.join_group_call(
        chat_id,
        InputStream(
            AudioPiped(url)
        )
    )
    await msg.edit(f"🎶 Now Playing: `{title}`")

@app.on_message(filters.command("stop") & filters.group)
async def stop(_, message: Message):
    await vc.leave_group_call(message.chat.id)
    await message.reply("⏹️ Stopped VC stream.")

vc.start()
app.run()
