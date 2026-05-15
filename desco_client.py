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
                    logger.info(f"Targeting customer portal: {self.CUSTOMER_PORTAL}")
                    page.goto(self.CUSTOMER_PORTAL, timeout=60000)
                    
                    # Wait for form elements (SPA might take a second)
                    page.wait_for_selector("input[name='account_no'], input[id='account_no']", timeout=15000)
                    
                    # Fill Account Number
                    page.fill("input[name='account_no'], input[id='account_no']", self.username)
                    
                    if self.meter_no:
                        # Some forms might need meter number too
                        meter_input = page.locator("input[name='meter_no'], input[id='meter_no']")
                        if meter_input.is_visible():
                            meter_input.fill(self.meter_no)
                    
                    logger.info("Submitting inquiry on customer portal...")
                    page.click("button:has-text('Submit'), button[type='submit'], input[type='submit']")
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
