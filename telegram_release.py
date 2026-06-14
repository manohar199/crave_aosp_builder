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

download_links = [f"<a href='{ROM_URL}'>ROM</a>"]

if BOOT_URL:
    download_links.append(f"<a href='{BOOT_URL}'>Boot</a>")

if VENDOR_BOOT_URL:
    download_links.append(f"<a href='{VENDOR_BOOT_URL}'>Vendor_Boot</a>")

if DTBO_URL:
    download_links.append(f"<a href='{DTBO_URL}'>dtbo</a>")

download_text = " || ".join(download_links)

caption = f"""
<b>{ROM_NAME}</b>

Updated: {BUILD_DATE}

Download: {download_text}
"""

if CHANGELOG_URL:
    caption += f"\nChangelog: <a href='{CHANGELOG_URL}'>Changelogs</a>"

if NOTES:
    caption += f"\nNotes: {NOTES}"

if MAINTAINER:
    caption += f"\n\nMaintainer: {MAINTAINER}"

if CREDITS:
    caption += f"\nCredits: {CREDITS}"

if DEVICE:
    caption += f"\nDevice: {DEVICE}"

if ROM_SIZE:
    caption += f"\nSize: {ROM_SIZE}"

if BANNER_IMAGE:
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
