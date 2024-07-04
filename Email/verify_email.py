import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import os

# SMTP_SERVER = os.getenv("SMTP_SERVER")
# SMTP_PORT = os.getenv("SMTP_PORT")
# SMTP_USERNAME = os.getenv("SMTP_USERNAME")
# SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
# FROM_EMAIL = os.getenv("FROM_EMAIL")

def send_verification_link(to_email, link):
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    SMTP_USERNAME = 'vyankatesht246@gmail.com'  
    SMTP_PASSWORD = 'blpjenkognaefeep' 
    FROM_EMAIL = 'vyankatesht246@gmail.com' 
    TO_EMAIL = to_email

    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL
    msg['Subject'] = "This is Your Varification Link"

    # Email body
    body = f'Click on this link to verify your email: {link}'
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Start TLS encryption (if supported by the server)
        server.login(SMTP_USERNAME, SMTP_PASSWORD)

        # Send the email
        server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())

        # Close the SMTP server connection
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

