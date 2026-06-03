# GoFile Telegram Bot — GitHub Actions Edition

A Telegram bot that receives files from users, uploads them to [GoFile.io](https://gofile.io), and returns a shareable download link. Runs entirely on **GitHub Actions** — no server required.

---

## Setup

### 1. Fork or push this repo to GitHub

### 2. Add GitHub Secrets

Go to your repo → **Settings → Secrets and variables → Actions → New repository secret** and add:

| Secret Name          | Description                                      | Required |
|----------------------|--------------------------------------------------|----------|
| `TELEGRAM_BOT_TOKEN` | Bot token from [@BotFather](https://t.me/BotFather) | ✅ Yes |
| `TELEGRAM_CHAT_ID`   | Chat/channel/group ID to log uploaded files      | ✅ Yes   |
| `TELEGRAM_API_ID`    | From [my.telegram.org](https://my.telegram.org)  | ✅ Yes   |
| `TELEGRAM_API_HASH`  | From [my.telegram.org](https://my.telegram.org)  | ✅ Yes   |
| `MUST_JOIN`          | Username/ID of channel users must join (optional)| ❌ No    |
| `DATABASE_URL`       | PostgreSQL URL for ban/stats features (optional) | ❌ No    |

### 3. Run the bot

Go to **Actions → Run GoFile Telegram Bot → Run workflow**

- Enter how many minutes to run (default: 60, max: 350)
- Click **Run workflow**

Or push to `main`/`master` to start automatically.

---

## How it works

```
User sends file to bot
        ↓
Bot downloads file from Telegram
        ↓
Bot uploads file to GoFile.io
        ↓
Bot sends GoFile link back to user
        ↓
A copy is forwarded to TELEGRAM_CHAT_ID (your log channel)
```

---

## Files changed from original

| File | Change |
|------|--------|
| `Config.py` | Now reads `TELEGRAM_API_ID`, `TELEGRAM_API_HASH`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` from env |
| `bot.py` | Added secret validation with clear error messages |
| `GoFileBot/main.py` | Uses `Config.CHAT_ID` for forwarding; improved error handling & progress updates |
| `.github/workflows/run-bot.yml` | New — runs the bot on GitHub Actions |
| `README.md` | This file |
