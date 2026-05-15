import logging
from playwright.sync_api import sync_playwright
from config import Config

logger = logging.getLogger(__name__)

class DescoClient:
    # Use the public inquiry URL if possible, otherwise use the main portal
    MAIN_URL = "https://prepaid.desco.org.bd/"
    CUSTOMER_PORTAL = "https://prepaid.desco.org.bd/customer/#/customer-info"

    def __init__(self):
        self.username = Config.DESCO_USER
        self.password = Config.DESCO_PASS
        self.meter_no = Config.METER_NUMBER

    def fetch_balance(self):
        """
        Fetches current balance using the customer info portal or login page.
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            )
            page = context.new_page()

            try:
                # Prioritize the Customer Portal if no password is used
                if not self.password:
                    logger.info(f"Targeting customer portal for inquiry: {self.CUSTOMER_PORTAL}")
                    page.goto(self.CUSTOMER_PORTAL, timeout=60000)
                    
                    # Wait for form (SPA might take a second)
                    page.wait_for_selector("input", timeout=15000)
                    
                    # If user provided username (Account No), use it
                    if self.username:
                        logger.info(f"Filling Account Number: {self.username}")
                        page.fill("input[placeholder*='Account'], input[name*='account'], input[id*='account']", self.username)
                    
                    # If user provided Meter Number specifically, or as a fallback
                    if self.meter_no:
                        logger.info(f"Filling Meter Number: {self.meter_no}")
                        page.fill("input[placeholder*='Meter'], input[name*='meter'], input[id*='meter']", self.meter_no)
                    
                    logger.info("Submitting inquiry...")
                    submit_button = page.locator("button:has-text('Search'), button:has-text('Submit'), button:has-text('Inquiry'), button[type='submit'], .btn-primary, .btn-search").first
                    
                    if submit_button.is_visible():
                        submit_button.click()
                    else:
                        logger.warning("Submit button not found by text, trying to press Enter...")
                        page.keyboard.press("Enter")
                else:
                    logger.info(f"Password provided. Navigating to main login: {self.MAIN_URL}")
                    page.goto(self.MAIN_URL, timeout=60000)
                    page.fill("input[name='userid'], input[name='username'], input[id='userid']", self.username)
                    page.fill("input[name='password'], input[id='password']", self.password)
                    logger.info("Attempting login...")
                    page.click("button[type='submit'], input[type='submit']")
                
                # Patient wait logic for SPA loading
                logger.info("Waiting for results to populate...")
                page.wait_for_load_state("networkidle", timeout=30000)
                
                import time
                import re
                from datetime import datetime
                
                balance = None
                meter_no = Config.METER_NUMBER
                start_time = time.time()
                while time.time() - start_time < 20:
                    balance_text = page.inner_text("body")
                    
                    # Regex patterns for balance: "Balance: 1,234.56" or "1,234 BDT"
                    patterns = [
                        r"(?:Balance|Current|Available|Amount)[^\d]*([\d,]+\.?\d*)",
                        r"([\d,]+\.?\d*)\s*(?:BDT|Tk|TK|Taka)"
                    ]
                    
                    found_val = None
                    for pattern in patterns:
                        for match in re.finditer(pattern, balance_text, re.I):
                            try:
                                val = float(match.group(1).replace(',', ''))
                                # Heuristic: Prioritize non-zero values during async loading
                                if found_val is None or val > 0:
                                    found_val = val
                            except: continue
                    
                    if found_val is not None and found_val > 0:
                        balance = found_val
                        meter_match = re.search(r"Meter\s*(?:No|Number)?\s*:?\s*(\d+)", balance_text, re.I)
                        if meter_match: meter_no = meter_match.group(1)
                        logger.info(f"Detected valid balance: {balance}")
                        break
                    
                    time.sleep(3)
                
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                if balance is not None:
                    logger.info(f"Successfully fetched balance: {balance} BDT")
                    return balance, meter_no, timestamp
                else:
                    logger.error("Failed to extract balance numeric value after waiting 20s.")
                    page.screenshot(path="logs/error_screenshot.png")
                    return None

            except Exception as e:
                logger.error(f"Error during scraping: {e}")
                page.screenshot(path="logs/critical_error.png")
                return None
            finally:
                browser.close()
