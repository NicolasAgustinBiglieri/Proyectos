import smtplib
from jose import jwt
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import settings

def create_verify_token(username, email):
    verification_token = {"username": username, "email": email}
    return jwt.encode(verification_token, settings.SECRET, algorithm=settings.ALGORITHM)

def send_email_verification(email, token):
    sender_email = settings.EMAIL_ACCOUNT
    password = settings.EMAIL_PASSWORD

    subject = "Verificación de registro"
    body = f"Por favor, haga clic en el siguiente enlace para verificar su registro: http://127.0.0.1:8000/auth/verify?token={token}"

    message = MIMEMultipart()
    message["from"] = sender_email
    message["To"] = email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, email, message.as_string())


