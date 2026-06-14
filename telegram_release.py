```python
import os
import requests

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

ROM_NAME = os.environ["ROM_NAME"]
BUILD_DATE = os.environ["BUILD_DATE"]

ROM_URL = os.environ["ROM_URL"]
RECOVERY_URL = os.environ.get("RECOVERY_URL", "")
BOOT_URL = os.environ.get("BOOT_URL", "")
VENDOR_BOOT_URL = os.environ.get("VENDOR_BOOT_URL", "")
DTBO_URL = os.environ.get("DTBO_URL", "")

BANNER_IMAGE = os.environ.get("BANNER_IMAGE", "")

CAPTION_TEXT = os.environ.get(
    "CAPTION_TEXT",
    "PROXIMA BETA Release"
)

CREDITS = os.environ.get(
    "CREDITS",
    "AxionOS Team\nVOLD_NAMESPACE"
)

MAINTAINER = os.environ.get(
    "MAINTAINER",
    "@Cmanohar2"
)

caption = f"""
{ROM_NAME}

Caption:
{CAPTION_TEXT}

Updated:
{BUILD_DATE}

Download:
ROM: {ROM_URL}
Recovery: {RECOVERY_URL}
Boot: {BOOT_URL}
Vendor_Boot: {VENDOR_BOOT_URL}
dtbo: {DTBO_URL}

Credits:
{CREDITS}

Maintainer:
{MAINTAINER}
""".strip()

if BANNER_IMAGE:
    response = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
        data={
            "chat_id": CHAT_ID,
            "photo": BANNER_IMAGE,
            "caption": caption
        }
    )
else:
    response = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": caption
        }
    )

print(response.text)
```
