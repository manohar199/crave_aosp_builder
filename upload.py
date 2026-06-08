import os
import sys
import requests

FILE_URL = os.environ["FILE_URL"]
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

OUTPUT_FILE = "download.bin"

print("=" * 60)
print("Downloading File")
print("=" * 60)

headers = {
    "User-Agent": "Mozilla/5.0"
}

with requests.get(FILE_URL, headers=headers, stream=True, allow_redirects=True) as r:
    r.raise_for_status()

    with open(OUTPUT_FILE, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)

size = os.path.getsize(OUTPUT_FILE)

print(f"Downloaded: {size / (1024**3):.2f} GB")

if size < 1024:
    print("Download failed")
    sys.exit(1)

print("=" * 60)
print("Uploading to Telegram")
print("=" * 60)

response = requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument",
    data={
        "chat_id": CHAT_ID,
        "caption": f"Size: {size/(1024**3):.2f} GB"
    },
    files={
        "document": open(OUTPUT_FILE, "rb")
    },
    timeout=7200
)

print(response.text)

if not response.ok:
    sys.exit(1)

print("Done")
