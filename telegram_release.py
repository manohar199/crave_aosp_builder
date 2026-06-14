import os
import requests

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

ROM_NAME = os.environ["ROM_NAME"]
MAINTAINER = os.environ.get("MAINTAINER", "")
CREDITS = os.environ.get("CREDITS", "")
NOTES = os.environ.get("NOTES", "")

ROM_SIZE = os.environ.get("ROM_SIZE", "")
DEVICE = os.environ.get("DEVICE", "")
BUILD_DATE = os.environ.get("BUILD_DATE", "")

BANNER_IMAGE = os.environ.get("BANNER_IMAGE", "")

ROM_URL = os.environ["ROM_URL"]
RECOVERY_URL = os.environ.get("RECOVERY_URL", "")
BOOT_URL = os.environ.get("BOOT_URL", "")
VENDOR_BOOT_URL = os.environ.get("VENDOR_BOOT_URL", "")
DTBO_URL = os.environ.get("DTBO_URL", "")
CHANGELOG_URL = os.environ.get("CHANGELOG_URL", "")

# Download links
download_text = f"<a href='{ROM_URL}'>ROM</a>"

if RECOVERY_URL.strip():
    download_text += f" | <a href='{RECOVERY_URL}'>Recovery</a>"

if BOOT_URL.strip():
    download_text += f" | <a href='{BOOT_URL}'>Boot</a>"

if VENDOR_BOOT_URL.strip():
    download_text += f" | <a href='{VENDOR_BOOT_URL}'>Vendor_Boot</a>"

if DTBO_URL.strip():
    download_text += f" | <a href='{DTBO_URL}'>dtbo</a>"

caption = f"""<b>{ROM_NAME}</b>

Updated: {BUILD_DATE}

Download: {download_text}
"""

if CHANGELOG_URL.strip():
    caption += f"\nChangelog: <a href='{CHANGELOG_URL}'>Changelogs</a>"

if NOTES.strip():
    caption += f"\nNotes: {NOTES}"

if MAINTAINER.strip():
    caption += f"\n\nMaintainer: {MAINTAINER}"

if CREDITS.strip():
    caption += f"\nCredits: {CREDITS}"

if DEVICE.strip():
    caption += f"\nDevice: {DEVICE}"

if ROM_SIZE.strip():
    caption += f"\nSize: {ROM_SIZE}"

print("ROM_URL =", ROM_URL)
print("RECOVERY_URL =", RECOVERY_URL)
print("BOOT_URL =", BOOT_URL)
print("VENDOR_BOOT_URL =", VENDOR_BOOT_URL)
print("DTBO_URL =", DTBO_URL)

if BANNER_IMAGE.strip():
    response = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
        data={
            "chat_id": CHAT_ID,
            "photo": BANNER_IMAGE,
            "caption": caption,
            "parse_mode": "HTML"
        }
    )
else:
    response = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": caption,
            "parse_mode": "HTML"
        }
    )

print(response.text)
