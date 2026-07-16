import asyncio
import yt_dlp

from pyrogram import filters
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream, AudioQuality

from app import app, user, call


@app.on_message(filters.command("start"))
async def start(_, m):
    await m.reply("Music Bot Ready 🎵")


@app.on_message(filters.command("play"))
async def play(_, m):

    if len(m.command) < 2:
        return await m.reply("Use: /play song name")

    query = " ".join(m.command[1:])

    await user.join_chat(m.chat.id)

    ydl = {
        "format": "bestaudio",
        "quiet": True,
        "noplaylist": True
    }

    with yt_dlp.YoutubeDL(ydl) as y:
        info = y.extract_info(
            f"ytsearch:{query}",
            download=False
        )

        url = info["entries"][0]["url"]

    await call.play(
        m.chat.id,
        MediaStream(
            url,
            audio_parameters=AudioQuality.LOW
        )
    )

    await m.reply(f"▶️ Playing: {query}")


@app.on_message(filters.command("stop"))
async def stop(_, m):
    await call.leave_call(m.chat.id)
    await m.reply("Stopped ⏹️")


async def main():
    await user.start()
    await call.start()
    await app.start()

    print("Music Bot Started ✅")

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
