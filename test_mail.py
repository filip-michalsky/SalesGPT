import os
from salesgpt.tools  import send_email_with_gmail  # Adjust the import path as necessary
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()
# Set environment variables for the test
def send_simple_email(recipient_email, subject, body):
    try:
        sender_email = os.getenv("GMAIL_MAIL")
        app_password = os.getenv("GMAIL_APP_PASSWORD")
        print(sender_email)
        print(app_password)
        # Ensure sender email and app password are not None
        if not sender_email or not app_password:
            return "Sender email or app password not set."

        # Create MIME message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Create server object with SSL option
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        return "Email sent successfully."
    except Exception as e:
        return f"Failed to send email: {e}"

# Test email details
recipient_email = "makovoz.ilja@gmail.com"
subject = "Test Email"
body = "This is a test email sent from the Python script without using LLM."

# Send the test email
result = send_simple_email(recipient_email, subject, body)
print(result)