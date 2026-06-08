import os
import json
import requests

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

ROM_NAME = os.environ["ROM_NAME"]
ROM_SIZE = os.environ["ROM_SIZE"]
DEVICE = os.environ["DEVICE"]
BUILD_DATE = os.environ["BUILD_DATE"]
MD5 = os.environ["MD5"]

BANNER_IMAGE = os.environ.get("BANNER_IMAGE", "")

ROM_URL = os.environ["ROM_URL"]
RECOVERY_URL = os.environ.get("RECOVERY_URL", "")
BOOT_URL = os.environ.get("BOOT_URL", "")
INIT_BOOT_URL = os.environ.get("INIT_BOOT_URL", "")
VENDOR_BOOT_URL = os.environ.get("VENDOR_BOOT_URL", "")
DTBO_URL = os.environ.get("DTBO_URL", "")

caption = f"""
🎁 A fresh package awaits your device!

• ROM: {ROM_NAME}
• SIZE: {ROM_SIZE}

• DEVICE: {DEVICE}
• DATE: {BUILD_DATE}

• MD5SUM: {MD5}
"""

buttons = []

buttons.append([{"text": "📦 Download ROM", "url": ROM_URL}])

if RECOVERY_URL:
    buttons.append([{"text": "🛠 Download Recovery", "url": RECOVERY_URL}])

if BOOT_URL:
    buttons.append([{"text": "⚡ Download Boot", "url": BOOT_URL}])

if INIT_BOOT_URL:
    buttons.append([{"text": "🚀 Download Init Boot", "url": INIT_BOOT_URL}])

if VENDOR_BOOT_URL:
    buttons.append([{"text": "🔧 Download Vendor Boot", "url": VENDOR_BOOT_URL}])

if DTBO_URL:
    buttons.append([{"text": "📁 Download DTBO", "url": DTBO_URL}])

keyboard = {
    "inline_keyboard": buttons
}

if BANNER_IMAGE:
    response = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
        data={
            "chat_id": CHAT_ID,
            "photo": BANNER_IMAGE,
            "caption": caption,
            "reply_markup": json.dumps(keyboard)
        }
    )
else:
    response = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": caption,
            "reply_markup": json.dumps(keyboard)
        }
    )

print(response.text)
