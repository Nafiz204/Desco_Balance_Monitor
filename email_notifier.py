import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config

logger = logging.getLogger(__name__)

class EmailNotifier:
    def __init__(self):
        self.user = Config.EMAIL_USER
        self.password = Config.EMAIL_PASS
        self.to_email = Config.EMAIL_TO
        self.smtp_server = Config.SMTP_SERVER
        self.smtp_port = Config.SMTP_PORT

    def send_alert(self, balance, threshold, meter_number, timestamp):
        subject = f"DESCO Balance Alert: Low Balance Warning ({balance} BDT)"
        
        body = f"""
        <html>
        <body>
            <h3>DESCO Low Balance Alert</h3>
            <p>Your electricity balance has fallen below the threshold.</p>
            <ul>
                <li><strong>Current Balance:</strong> {balance} BDT</li>
                <li><strong>Threshold Breached:</strong> {threshold} BDT</li>
                <li><strong>Meter Number:</strong> {meter_number}</li>
                <li><strong>Time Checked:</strong> {timestamp}</li>
            </ul>
            <p>Please recharge your meter soon to avoid disconnection.</p>
            <br>
            <p><small>This is an automated message from your DESCO Monitoring System.</small></p>
        </body>
        </html>
        """
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.user
            msg['To'] = self.to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html'))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.user, self.password)
                server.send_message(msg)
                
            logger.info(f"Alert email sent to {self.to_email} for balance {balance} BDT")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
