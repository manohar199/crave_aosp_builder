import os
import asyncio
import requests
from telethon import TelegramClient

FILE_URL = os.environ["FILE_URL"]

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = int(os.environ["TELEGRAM_CHAT_ID"])

API_ID = int(os.environ["TELEGRAM_API_ID"])
API_HASH = os.environ["TELEGRAM_API_HASH"]

print("=" * 60)
print("Downloading file")
print("=" * 60)

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(
    FILE_URL,
    headers=headers,
    stream=True,
    allow_redirects=True,
    timeout=60
)

response.raise_for_status()

filename = FILE_URL.split("/")[-1]

if not filename:
    filename = "downloaded_file"

with open(filename, "wb") as f:
    for chunk in response.iter_content(chunk_size=1024 * 1024):
        if chunk:
            f.write(chunk)

size = os.path.getsize(filename)

print(f"Filename: {filename}")
print(f"Size: {size / 1024 / 1024:.2f} MB")

if size < 50000:
    raise Exception("Downloaded file too small")

print("=" * 60)
print("Uploading to Telegram")
print("=" * 60)

print("CHAT_ID =", CHAT_ID)
print("CHAT_ID TYPE =", type(CHAT_ID))

async def upload():
    client = TelegramClient(
        "bot_session",
        API_ID,
        API_HASH
    )

    await client.start(bot_token=BOT_TOKEN)

    me = await client.get_me()
    print("Bot Username:", me.username)

    await client.send_file(
        CHAT_ID,
        filename,
        caption=filename
    )

    await client.disconnect()

asyncio.run(upload())

print("=" * 60)
print("Upload Complete")
print("=" * 60)
