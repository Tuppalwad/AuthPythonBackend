import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# # SMTP server settings
# SMTP_SERVER = os.getenv("SMTP_SERVER")
# SMTP_PORT = os.getenv("SMTP_PORT")
# SMTP_USERNAME = os.getenv("SMTP_USERNAME")
# SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# FROM_EMAIL_ID = 'info@supervc.in'

def forgot_password_email(to_email, link):
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    SMTP_USERNAME = 'vyankatesht246@gmail.com'  
    SMTP_PASSWORD = 'blpjenkognaefeep' 
    FROM_EMAIL = 'vyankatesht246@gmail.com' 
    TO_EMAIL = to_email
    # Create a MIME message
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email
    msg['Subject'] = 'Password Reset'

    # Email body
    body = f'Click the following link to reset your password: {link}'
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Start TLS encryption (if supported by the server)
        server.login(SMTP_USERNAME, SMTP_PASSWORD)

        # Send the email
        server.sendmail(FROM_EMAIL, to_email, msg.as_string())

        # Close the SMTP server connection
        server.quit()
        
        print("Email sent successfully")
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

