import os
import asyncio
import requests
from telethon import TelegramClient

FILE_URL = os.environ["FILE_URL"]

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

API_ID = int(os.environ["TELEGRAM_API_ID"])
API_HASH = os.environ["TELEGRAM_API_HASH"]

print("=" * 60)
print("Downloading file")
print("=" * 60)

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(
    FILE_URL,
    headers=headers,
    stream=True,
    allow_redirects=True,
    timeout=60
)

r.raise_for_status()

filename = FILE_URL.split("/")[-1]

if not filename:
    filename = "downloaded_file"

with open(filename, "wb") as f:
    for chunk in r.iter_content(chunk_size=1024 * 1024):
        if chunk:
            f.write(chunk)

size = os.path.getsize(filename)

print("Filename:", filename)
print("Size:", round(size / 1024 / 1024, 2), "MB")

if size < 50000:
    raise Exception("Downloaded file too small")

print("=" * 60)
print("Uploading to Telegram")
print("=" * 60)

async def upload():
    client = TelegramClient(
        "bot_session",
        API_ID,
        API_HASH
    )

    await client.start(bot_token=BOT_TOKEN)

    await client.send_file(
        entity=CHAT_ID,
        file=filename,
        caption=filename,
        part_size_kb=512
    )

    await client.disconnect()

asyncio.run(upload())

print("=" * 60)
print("Upload Complete")
print("=" * 60)
