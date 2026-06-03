import os
import requests

FILE_URL = os.environ["FILE_URL"]
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

filename = "downloaded_file"

print("Downloading:", FILE_URL)

r = requests.get(FILE_URL, stream=True, allow_redirects=True)

print("Status:", r.status_code)
print("Content-Type:", r.headers.get("content-type"))

r.raise_for_status()

with open(filename, "wb") as f:
    for chunk in r.iter_content(8192):
        if chunk:
            f.write(chunk)

size = os.path.getsize(filename)

print("Downloaded size:", size, "bytes")

if size < 10000:
    print("WARNING: File is suspiciously small")

    with open(filename, "rb") as f:
        print(f.read(500).decode(errors="ignore"))

print("Uploading to Telegram...")

with open(filename, "rb") as f:
    resp = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument",
        data={"chat_id": CHAT_ID},
        files={"document": f}
    )

print("Telegram response:")
print(resp.text)
