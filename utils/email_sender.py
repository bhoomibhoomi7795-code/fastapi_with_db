import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
load_dotenv()
app_password = os.environ["APP_PASSWORD"]
sender_email = os.environ["SENDER_EMAIL"]

# Email details
def send_email(receiver_email: str, subject: str, content: str) -> None:
    """Send an email to the specified receiver with the given subject and content."""
   
# Create email
    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.set_content(content)

    # Send email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()  # secure connection  
        server.login(sender_email, app_password)
        server.send_message(msg)

    print("Email sent successfully!")
