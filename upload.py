import os
import sys
import requests

FILE_URL = os.environ["FILE_URL"]
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

headers = {
    "User-Agent": "Mozilla/5.0"
}

print("=" * 60)
print("Downloading file")
print("=" * 60)
print("URL:", FILE_URL)

r = requests.get(
    FILE_URL,
    headers=headers,
    stream=True,
    allow_redirects=True
)

print("Status:", r.status_code)
print("Content-Type:", r.headers.get("content-type"))
print("Final URL:", r.url)

filename = FILE_URL.split("/")[-1]

with open(filename, "wb") as f:
    for chunk in r.iter_content(chunk_size=1024 * 1024):
        if chunk:
            f.write(chunk)

size = os.path.getsize(filename)

print(f"Filename: {filename}")
print(f"Size: {size} bytes")
print(f"Size: {size/1024/1024:.2f} MB")

# Detect HTML page instead of real file
if size < 50000:
    print("\n===== FILE CONTENT PREVIEW =====\n")
    with open(filename, "rb") as f:
        preview = f.read(2000)
        print(preview.decode(errors="ignore"))
    print("\n================================")
    sys.exit("Downloaded page instead of file")

print("=" * 60)
print("Uploading to Telegram")
print("=" * 60)

with open(filename, "rb") as f:
    response = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument",
        data={
            "chat_id": CHAT_ID,
            "caption": filename
        },
        files={
            "document": (filename, f)
        },
        timeout=7200
    )

print("Telegram Response:")
print(response.text)

if not response.ok:
    sys.exit("Telegram upload failed")

print("Done")
