import os
import sys
import asyncio
from telethon import TelegramClient

API_ID = os.environ.get('TELEGRAM_API_ID')
API_HASH = os.environ.get('TELEGRAM_API_HASH')
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
TARGET_PATH = os.environ.get('TARGET_PATH')

async def main():
    # Verify all secrets are present
    if not all([API_ID, API_HASH, BOT_TOKEN, CHAT_ID, TARGET_PATH]):
        print("Error: Missing required environment variables.")
        sys.exit(1)
        
    # Initialize the client using API ID and Hash
    client = TelegramClient('bot_session', int(API_ID), API_HASH)
    await client.start(bot_token=BOT_TOKEN)
    
    try:
        # Format chat ID safely
        chat_id = int(CHAT_ID) if CHAT_ID.lstrip('-').isdigit() else CHAT_ID
        
        # Determine files to upload
        files_to_upload = []
        if os.path.isfile(TARGET_PATH):
            files_to_upload.append(TARGET_PATH)
        elif os.path.isdir(TARGET_PATH):
            for root, _, files in os.walk(TARGET_PATH):
                for f in files:
                    files_to_upload.append(os.path.join(root, f))
        else:
            print(f"Path {TARGET_PATH} does not exist.")
            sys.exit(1)

        if not files_to_upload:
            print("No files found to upload.")
            sys.exit(0)

        # Upload sequence
        for file_path in files_to_upload:
            print(f"Uploading {file_path} to chat {chat_id}...")
            await client.send_file(
                chat_id, 
                file_path, 
                caption=f"Uploaded via GitHub Actions: {os.path.basename(file_path)}"
            )
            print(f"Success: {file_path}")

    except Exception as e:
        print(f"Error during upload: {e}")
        sys.exit(1)
    finally:
        await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
