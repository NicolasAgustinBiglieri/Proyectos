import smtplib
from jose import jwt
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
from config import settings
from db.logger_base import log
from services.users_service import search_user
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status
from smtplib import SMTPAuthenticationError
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


from dotenv import load_dotenv
load_dotenv()


def create_verify_token(username, email):
    """
    Crear un token de verificación para el usuario.
    """
    verification_token = {"username": username, "email": email}
    return jwt.encode(verification_token, settings.SECRET, algorithm=settings.ALGORITHM)


sender_email = settings.EMAIL_ACCOUNT
password = settings.EMAIL_PASSWORD

sendgrid_api_key = settings.SENDGRID_API_KEY


# def send_email_verification(email, token):
#     """
#     Enviar un correo de verificación al usuario.
#     """
#     subject = "Verificación de registro"
#     body = f"Por favor, haga clic en el siguiente enlace para verificar su registro: http://127.0.0.1:8000/auth/verify?token={token}"

#     message = MIMEMultipart()
#     message["from"] = sender_email
#     message["To"] = email
#     message["Subject"] = subject
#     message.attach(MIMEText(body, "plain"))

#     try:    
#         with smtplib.SMTP("smtp.gmail.com", 587) as server:
#             server.starttls()
#             server.login(sender_email, password)
#             server.sendmail(sender_email, email, message.as_string())
#     except Exception as e:
#         log.error(f"Error al enviar el correo de verificación: {e}")
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error desconocido")




def send_email_verification(email, token):
    # Configura tu API Key de SendGrid

    subject = "Verificación de registro"
    body = f"Por favor, haga clic en el siguiente enlace para verificar su registro: http://127.0.0.1:8000/auth/verify?token={token}"

    message = Mail(
        from_email=sender_email,  # Usa un correo verificado en SendGrid
        to_emails=email,
        subject=subject,
        html_content=body  # El contenido del correo en HTML
    )

    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
        log.info(f"Correo enviado a {email}, {response.status_code}")
        return response.status_code
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return None






def send_password_reset_email(email):
    """
    Enviar un correo de recuperación de contraseña al usuario.
    """
    try:
        user = search_user("email", email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "No se ha encontrado el usuario")
        
        expire = datetime.now(timezone.utc) + timedelta(hours=1)
        verification_token = {"username": user.username, "email": user.email, "exp": expire}
        token = jwt.encode(verification_token, settings.SECRET, algorithm=settings.ALGORITHM)

        subject = "Recuperación de contraseña"
        body = (
            f"Por favor, haga clic en el siguiente enlace para recuperar su contraseña: "
            f"http://127.0.0.1:8000/reset-password?token={token}"
            "\n\nEste enlace expirará en 1 hora."
        )

        message = Mail(
            from_email=sender_email,  # Usa un correo verificado en SendGrid
            to_emails=email,
            subject=subject,
            html_content=body  # El contenido del correo en HTML
        )
 
        try:
            sg = SendGridAPIClient(sendgrid_api_key)
            response = sg.send(message)
            log.info(f"Correo de recuperación de contraseña enviado a {email}, {response.status_code}")
            return response.status_code
        except Exception as e:
            print(f"Error al enviar correo: {e}")
            return None
        
        

    except ValueError as ve:
        log.error(f"Error al enviar correo de recuperación de contraseña: {ve}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    except smtplib.SMTPException as smtp_e:
        log.error(f"Error al enviar correo de recuperación de contraseña: {smtp_e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al enviar correo electrónico")
    except SMTPAuthenticationError as e:
        log.error(f"Error de autenticación en SMTP: {smtp_e}")
        raise RuntimeError(f"Error de autenticación en SMTP: {e}")
    except Exception as e:
        log.error(f"Error desconocido al enviar correo de recuperación de contraseña: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error desconocido")

