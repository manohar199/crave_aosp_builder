import os
import asyncio
from pyrogram import Client

API_ID = int(os.environ["TELEGRAM_API_ID"])
API_HASH = os.environ["TELEGRAM_API_HASH"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

DOWNLOAD_DIR = "downloads"

async def main():
    app = Client(
        "github_uploader",
        api_id=API_ID,
        api_hash=API_HASH,
        in_memory=True
    )

    await app.start()

    for root, dirs, files in os.walk(DOWNLOAD_DIR):
        for file in files:
            path = os.path.join(root, file)

            try:
                size = os.path.getsize(path)

                if size > 0:
                    print(f"Uploading: {path}")

                    await app.send_document(
                        chat_id=CHAT_ID,
                        document=path,
                        caption=file
                    )

            except Exception as e:
                print(f"Failed upload: {path}")
                print(e)

    await app.stop()

asyncio.run(main())
