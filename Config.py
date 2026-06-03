import os

# ── Reads all credentials from environment variables ────────────────────────
# Set these in GitHub → Settings → Secrets and variables → Actions

try:
    API_ID = int(os.environ.get('TELEGRAM_API_ID', 0))
except ValueError:
    raise Exception("TELEGRAM_API_ID must be a valid integer.")

API_HASH    = os.environ.get('TELEGRAM_API_HASH', None)
BOT_TOKEN   = os.environ.get('TELEGRAM_BOT_TOKEN', None)
CHAT_ID     = os.environ.get('TELEGRAM_CHAT_ID', None)

# Optional: username or ID of a channel users must join before using the bot
MUST_JOIN   = os.environ.get('MUST_JOIN', None)
if MUST_JOIN and MUST_JOIN.startswith("@"):
    MUST_JOIN = MUST_JOIN[1:]

# Optional: PostgreSQL database URL (only needed if you use ban/stats features)
# Format: postgresql://user:password@host:port/dbname
DATABASE_URL = os.environ.get('DATABASE_URL', None)
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    # SQLAlchemy dropped support for the "postgres://" prefix
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
