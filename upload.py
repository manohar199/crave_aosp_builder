import os
import re
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

# Extract Google Drive File ID
match = re.search(r'id=([a-zA-Z0-9_-]+)', FILE_URL)

if not match:
    print("Could not extract Google Drive file ID")
    sys.exit(1)

file_id = match.group(1)

print("File ID:", file_id)

try:
    gdown.download(
        id=file_id,
        output=OUTPUT_FILE,
        quiet=False
    )
except Exception as e:
    print("Download failed:", e)
    sys.exit(1)

if not os.path.exists(OUTPUT_FILE):
    print("Downloaded file not found")
    sys.exit(1)

size = os.path.getsize(OUTPUT_FILE)

print(f"Downloaded Size: {size / (1024**3):.2f} GB")

if size < 100 * 1024 * 1024:
    print("Downloaded file is too small.")
    print("Probably Google Drive returned HTML instead of ROM ZIP.")
    sys.exit(1)

print("=" * 60)
print("Uploading to Telegram")
print("=" * 60)

telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"

with open(OUTPUT_FILE, "rb") as f:
    response = requests.post(
        telegram_url,
        data={
            "chat_id": CHAT_ID,
            "caption": f"ROM ZIP ({size/(1024**3):.2f} GB)"
        },
        files={
            "document": f
        },
        timeout=7200
    )

print("Telegram Response:")
print(response.text)

if response.status_code != 200:
    sys.exit(1)

print("=" * 60)
print("Completed Successfully")
print("=" * 60)
