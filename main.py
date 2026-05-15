import logging
import json
import os
from datetime import datetime
from config import Config
from desco_client import DescoClient
from email_notifier import EmailNotifier

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/monitor.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_last_status():
    if os.path.exists(Config.STATE_FILE):
        try:
            with open(Config.STATE_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_status(status):
    with open(Config.STATE_FILE, 'w') as f:
        json.dump(status, f, indent=4)

def check_balance():
    logger.info("Starting DESCO Balance Check...")
    
    try:
        Config.validate()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return

    client = DescoClient()
    result = client.fetch_balance()

    last_status = load_last_status()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not result:
        logger.error("Failed to fetch balance. Check logs and screenshots.")
        last_status["last_check_status"] = "failed"
        last_status["last_check_time"] = timestamp
        save_status(last_status)
        return

    balance, meter_no, timestamp = result

    # Check thresholds
    triggered_threshold = None
    for threshold in sorted(Config.THRESHOLDS, reverse=True):
        if balance < threshold:
            # Avoid duplicate alerts for the same threshold if balance hasn't increased since
            last_threshold = last_status.get("last_alert_threshold")
            last_balance = last_status.get("balance", 0)
            
            # Send alert if:
            # 1. This is a lower threshold than before
            # 2. Or if balance was previously above this threshold
            if last_threshold is None or threshold < last_threshold or last_balance >= threshold:
                triggered_threshold = threshold
                break
    
    if triggered_threshold:
        logger.info(f"Low balance detected: {balance} BDT (Threshold: {triggered_threshold} BDT)")
        notifier = EmailNotifier()
        success = notifier.send_alert(balance, triggered_threshold, meter_no, timestamp)
        
        if success:
            last_status["last_alert_threshold"] = triggered_threshold
            last_status["last_alert_time"] = timestamp
    else:
        logger.info(f"Balance is healthy: {balance} BDT")
        # Clear alert threshold if balance is restored
        if balance >= max(Config.THRESHOLDS):
            last_status["last_alert_threshold"] = None

    # Update status
    last_status["balance"] = balance
    last_status["meter_no"] = meter_no
    last_status["last_check"] = timestamp
    save_status(last_status)
    
    logger.info("Check completed successfully.")

if __name__ == "__main__":
    check_balance()
