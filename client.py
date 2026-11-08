
import smtplib
import socket
from email.message import EmailMessage
from config import EMAIL, DESTINATION_HOST, DESTINATION_PORT

def trimite_email():
    destinatar = input("Destinatar: ").strip()
    subiect = input("Subiect: ").strip()
    continut = input("Mesaj: ").strip()

    if not destinatar or not subiect or not continut:
        print("Eroare: Toate campurile sunt obligatorii!")
        return

    mesaj = EmailMessage()
    mesaj["From"] = EMAIL
    mesaj["To"] = destinatar
    mesaj["Subject"] = subiect
    mesaj.set_content(continut)

    try:
        with smtplib.SMTP(DESTINATION_HOST, DESTINATION_PORT, timeout=5) as server:
            server.send_message(mesaj)

        print("Email trimis cu succes!")

    except smtplib.SMTPRecipientsRefused:
        print("Eroare: Destinatarul nu este acceptat de server!")

    except (ConnectionRefusedError, socket.timeout, OSError):
        print("Eroare: Nu se poate realiza conexiunea cu serverul SMTP!")

    except smtplib.SMTPException as eroare:
        print(f"Eroare SMTP: {eroare}")
