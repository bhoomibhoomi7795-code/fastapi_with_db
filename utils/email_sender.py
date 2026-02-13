import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
load_dotenv()
APP_PASSWORD = os.environ["APP_PASSWORD"]
SENDER_EMAIL = os.environ["SENDER_EMAIL"]

# Email details
def send_email(receiver_email: str, subject: str, content: str) -> None:
    """Send an email to the specified receiver with the given subject and content."""
   
# Create email
    msg = EmailMessage()
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.set_content(content)

    # Send email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()  # secure connection  
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)

    print("Email sent successfully!")
