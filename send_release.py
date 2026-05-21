import requests
import html
import os

# --- Configuration ---
# CHANGE THESE TWO LINES TO MATCH YOUR REPOSITORY
GITHUB_OWNER = 'manohar199'  
GITHUB_REPO = 'crave_aosp_builder'   

# These are securely injected by GitHub Actions
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
RELEASE_TAG = os.environ.get('RELEASE_TAG')
# ---------------------

def get_release_files():
    """Fetches the release assets using a specific tag or falls back to latest."""
    if RELEASE_TAG:
        url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/tags/{RELEASE_TAG}"
        print(f"Fetching exact release tag: {RELEASE_TAG}...")
    else:
        url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
        print("No RELEASE_TAG found. Fetching latest stable release...")
    
    response = requests.get(url)
    response.raise_for_status()
    release_data = response.json()
    
    files_content = {}
    
    for asset in release_data.get('assets', []):
        download_url = asset['browser_download_url']
        file_name = asset['name']
        print(f"Downloading {file_name}...")
        
        file_response = requests.get(download_url)
        file_response.raise_for_status()
        
        try:
            files_content[file_name] = file_response.text
        except Exception as e:
            print(f"Skipping {file_name} - not text: {e}")
            
    return files_content

def send_to_telegram(file_name, content):
    """Sends the file content to Telegram formatted inside a code box."""
    max_length = 4000 
    if len(content) > max_length:
        content = content[:max_length] + "\n\n... [TRUNCATED]"
        
    safe_content = html.escape(content)
    message = f"<b>File: {file_name}</b>\n<pre>{safe_content}</pre>"
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print(f"Failed to send {file_name}: {response.text}")
    else:
        print(f"Successfully sent {file_name} to Telegram.")

def main():
    try:
        # Fixed: Using the correct upgraded function name here
        files = get_release_files()
        
        if not files:
            print("No text-based release files found to process.")
            return
            
        for name, content in files.items():
            send_to_telegram(name, content)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
