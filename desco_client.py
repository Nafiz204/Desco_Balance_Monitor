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
                    # We try to find any input that might be for Account No or Meter No
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
                    # Try clicking multiple common search/submit patterns
                    submit_button = page.locator("button:has-text('Search'), button:has-text('Submit'), button:has-text('Inquiry'), button[type='submit'], .btn-primary, .btn-search").first
                    
                    if submit_button.is_visible():
                        submit_button.click()
                    else:
                        logger.warning("Submit button not found by text, trying to press Enter on input field...")
                        # Fallback: Press Enter on the last filled input field
                        page.keyboard.press("Enter")
                else:
                    logger.info(f"Password provided. Navigating to main login: {self.MAIN_URL}")
                    page.goto(self.MAIN_URL, timeout=60000)
                    
                    page.fill("input[name='userid'], input[name='username'], input[id='userid']", self.username)
                    page.fill("input[name='password'], input[id='password']", self.password)
                    
                    logger.info("Attempting login...")
                    page.click("button[type='submit'], input[type='submit']")
                
                # Wait for results - SPAs often take time to fetch data after button click
                page.wait_for_load_state("networkidle")
                # Wait a bit longer for the specific balance text to likely appear
                page.wait_for_timeout(3000) 
                
                # Extract balance
                # Usually balance is in a div or span with 'balance' in text or id
                balance_selector = ".balance-amount, #balance, :text('Balance')"
                balance_text = ""
                
                # Try to find balance specifically
                try:
                    # Look for elements containing "BDT" or numeric values near "Balance"
                    balance_element = page.locator("text=/Balance|Current Balance/i").first
                    if balance_element:
                        # Find the nearest numeric value
                        parent = balance_element.locator("xpath=..")
                        balance_text = parent.inner_text()
                except:
                    logger.warning("Could not find balance with text locator, trying generic extraction")
                
                # Fallback: Extract from whole page if specific selector fails
                if not balance_text:
                    balance_text = page.content()

                # Parse balance (simple regex approach in main or here)
                # For now, return the raw text or found value
                import re
                match = re.search(r"(\d+\.?\d*)\s*(?:BDT|Tk|TK)", balance_text)
                balance = float(match.group(1)) if match else None
                
                meter_match = re.search(r"Meter\s*(?:No|Number)?\s*:?\s*(\d+)", balance_text, re.I)
                meter_no = meter_match.group(1) if meter_match else Config.METER_NUMBER

                from datetime import datetime
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                if balance is not None:
                    logger.info(f"Successfully fetched balance: {balance} BDT")
                    return balance, meter_no, timestamp
                else:
                    logger.error("Failed to extract balance numeric value from page")
                    # Save a screenshot for debugging if it fails
                    page.screenshot(path="logs/error_screenshot.png")
                    return None

            except Exception as e:
                logger.error(f"Error during scraping: {e}")
                page.screenshot(path="logs/critical_error.png")
                return None
            finally:
                browser.close()
