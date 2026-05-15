import os
from dotenv import load_dotenv

# Load local .env file if it exists
load_dotenv()

class Config:
    # DESCO Credentials
    DESCO_USER = os.getenv("DESCO_USER")
    DESCO_PASS = os.getenv("DESCO_PASS")
    METER_NUMBER = os.getenv("METER_NUMBER")
    
    # Email Settings
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    EMAIL_TO = os.getenv("EMAIL_TO")
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    
    # Thresholds (in BDT)
    THRESHOLDS = [500, 200, 100]
    
    # Session Persistence (optional)
    STATE_FILE = "logs/status.json"

    @classmethod
    def validate(cls):
        # DESCO_PASS is now optional
        required = ["DESCO_USER", "EMAIL_USER", "EMAIL_PASS", "EMAIL_TO"]
        missing = [var for var in required if not getattr(cls, var)]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
