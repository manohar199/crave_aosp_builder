
import requests
import html
import os

GITHUB_OWNER = 'your_github_username'  
GITHUB_REPO = 'your_repository_name'   

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# NEW: Read the exact release tag from GitHub Actions
RELEASE_TAG = os.environ.get('RELEASE_TAG')

def get_release_files():
    # If a tag is provided, get that exact release. Otherwise, fall back to latest.
    if RELEASE_TAG:
        url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/tags/{RELEASE_TAG}"
        print(f"Fetching exact release: {RELEASE_TAG}...")
    else:
        url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
        print("Fetching latest stable release...")
    
    response = requests.get(url)
    response.raise_for_status()
    release_data = response.json()
    
    # ... (the rest of the script remains exactly the same) ... 
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
    max_length = 4000 
    if len(content) > max_length:
        content = content[:max_length] + "\n\n... [TRUNCATED]"
        
    safe_content = html.escape(content)
    message = f"File: {file_name}\n{safe_content}"
    
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
        print(f"Successfully sent {file_name}.")

def main():
    try:
        files = get_latest_release_files()
        if not files:
            print("No files found.")
            return
        for name, content in files.items():
            send_to_telegram(name, content)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
