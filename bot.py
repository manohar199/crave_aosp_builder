import Config
import logging
from pyrogram import Client, idle
from pyrogram.errors import ApiIdInvalid, ApiIdPublishedFlood, AccessTokenInvalid

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# Validate required secrets are present
if not Config.API_ID:
    raise Exception("TELEGRAM_API_ID secret is missing or 0.")
if not Config.API_HASH:
    raise Exception("TELEGRAM_API_HASH secret is missing.")
if not Config.BOT_TOKEN:
    raise Exception("TELEGRAM_BOT_TOKEN secret is missing.")

app = Client(
    ":memory:",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="GoFileBot"),
)

if __name__ == "__main__":
    try:
        app.start()
    except (ApiIdInvalid, ApiIdPublishedFlood):
        raise Exception("TELEGRAM_API_ID or TELEGRAM_API_HASH is invalid.")
    except AccessTokenInvalid:
        raise Exception("TELEGRAM_BOT_TOKEN is invalid.")
    uname = app.get_me().username
    print(f"@{uname} started successfully!")
    idle()
    app.stop()
    print("Bot stopped.")
