# DESCO Prepaid Balance Monitor

An automated system to monitor your DESCO prepaid electricity balance and receive email alerts when it falls below certain thresholds.

## Features

- **Automated Scraping:** Logs into the DESCO portal to fetch your current balance.
- **Email Alerts:** Sends notifications when balance drops below 500, 200, or 100 BDT.
- **Scheduled Monitoring:** Runs every day at 7:00 AM BST using GitHub Actions.
- **State Persistent:** Tracks alerts to avoid duplicate spamming.

## Setup Instructions

### 1. GitHub Secrets Configuration
To enable the GitHub Action, go to your repository **Settings > Secrets and variables > Actions** and add the following secrets:

| Secret Name | Description |
|---|---|
| `DESCO_USER` | Your DESCO **Account Number** (Consumer ID) |
| `DESCO_PASS` | (Optional) Your DESCO portal password. Leave empty if only Account No is needed for inquiry. |
| `METER_NUMBER` | Your **Meter Number** (Recommended for public inquiry) |
| `EMAIL_USER` | Your sender email address (e.g., `yourname@gmail.com`) |
| `EMAIL_PASS` | Your **App Password** (16-character code from Google Security settings) |
| `EMAIL_TO`   | The recipient email address for alerts |

### 2. Email Configuration Details (Gmail Example)
- **SMTP_SERVER**: `smtp.gmail.com`
- **SMTP_PORT**: `587`
- **EMAIL_PASS**: 
  1. Go to your [Google Account Settings](https://myaccount.google.com/).
  2. Search for "App Passwords".
  3. Create a new one for "Mail" and "Other (Custom Name)".
  4. Copy the **16-digit code** provided. This is your `EMAIL_PASS`. It allows the script to send emails bypasssing 2FA.

### 3. Recent Fixes
- **Dynamic Waiting (SPA Support)**: Implemented a 20-second polling loop that waits for balance data to populate. This solves issues where the script would read data before the DESCO portal's frontend finished fetching from the backend.
- **Improved Heuristics**: Better extraction logic that prioritizes non-zero values during page load to avoid capturing temporary placeholders.
- **Decimal & Comma Support**: Full support for balances with commas (e.g., `1,250.00 BDT`).
- **Debug Artifacts**: Screenshots and logs are now easier to trace via GitHub Actions artifacts.

### 4. Local Testing
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```
3. Create a `.env` file based on `.env.example`.
4. Run the script:
   ```bash
   python main.py
   ```

## How it Works

1. **Scraping:** The system uses `Playwright` to emulate a browser and navigate to the DESCO portal. It captures the balance amount using text patterns.
2. **Analysis:** It compares the current balance against defined thresholds (500, 200, 100).
3. **Notification:** If a threshold is breached, it sends an HTML-formatted email via SMTP.
4. **Logging:** Results are saved to `logs/status.json` and committed back to the repository to track the last alert state.

## Troubleshooting

- **Login Failed:** Check your `DESCO_USER` and `DESCO_PASS`. Some meters use a specific account number instead of the meter number for login.
- **Selector Issues:** Web portals often change. If the balance isn't found, check `logs/error_screenshot.png` (available if run locally or captured in CI artifacts).
- **Email Not Sending:** Ensure you are using an "App Password" and that `SMTP_SERVER` is correct.

## License
MIT
