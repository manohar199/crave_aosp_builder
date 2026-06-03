import os
import requests

FILE_URL = os.environ["FILE_URL"]

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

filename = "file.bin"

print("Downloading:", FILE_URL)

r = requests.get(FILE_URL, stream=True)
r.raise_for_status()

with open(filename, "wb") as f:
    for chunk in r.iter_content(8192):
        if chunk:
            f.write(chunk)

print("Sending to Telegram...")

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument",
    data={"chat_id": CHAT_ID},
    files={"document": open(filename, "rb")}
)

print("Done")
