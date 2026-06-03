import os
import sys
import gdown
import requests

FILE_URL = os.environ["FILE_URL"]
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

OUTPUT_FILE = "rom.zip"

print("=" * 60)
print("Downloading ROM from Google Drive")
print("=" * 60)

try:
    gdown.download(
        FILE_URL,
        OUTPUT_FILE,
        quiet=False,
        fuzzy=True
    )
except Exception as e:
    print(f"Download failed: {e}")
    sys.exit(1)

if not os.path.exists(OUTPUT_FILE):
    print("ROM file not found after download")
    sys.exit(1)

size = os.path.getsize(OUTPUT_FILE)

print(f"Downloaded size: {size / (1024**3):.2f} GB")

if size < 100 * 1024 * 1024:
    print("Downloaded file too small. Probably HTML page instead of ROM.")
    sys.exit(1)

print("=" * 60)
print("Uploading to Telegram")
print("=" * 60)

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"

with open(OUTPUT_FILE, "rb") as f:
    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "caption": f"ROM ZIP ({size/(1024**3):.2f} GB)"
        },
        files={
            "document": f
        },
        timeout=3600
    )

print("Telegram response:")
print(response.text)

if response.status_code != 200:
    sys.exit(1)

print("=" * 60)
print("Upload completed successfully")
print("=" * 60)
