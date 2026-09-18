import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
MAX_IMAGE_SIZE_MB = int(os.getenv("MAX_IMAGE_SIZE_MB", 20))
DEFAULT_JPEG_QUALITY = int(os.getenv("DEFAULT_JPEG_QUALITY", 95))

def validate_config():
    """Verify that essential configuration values are set."""
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        return False, "TELEGRAM_BOT_TOKEN is not set in your .env file."
    return True, "Configuration is valid."
