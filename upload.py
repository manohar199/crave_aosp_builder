import os
import requests

FILE_URL = os.environ["FILE_URL"]
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

filename = FILE_URL.split("/")[-1]

print("Downloading:", filename)

with requests.get(FILE_URL, stream=True) as r:
    r.raise_for_status()

    with open(filename, "wb") as f:
        for chunk in r.iter_content(1024 * 1024):
            if chunk:
                f.write(chunk)

size = os.path.getsize(filename)

print(f"Downloaded: {filename}")
print(f"Size: {size/1024/1024:.2f} MB")

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

print(response.text)
