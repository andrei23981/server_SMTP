
import smtplib
import socket

def verifica_conexiunea():
    try:
        with smtplib.SMTP("127.0.0.1", 1025, timeout=5) as server:
            cod, mesaj = server.noop()

            if cod == 250:
                print("Serverul SMTP este online!")
                print("Conexiunea functioneaza corect.")
            else:
                print(f"Serverul a raspuns cu codul: {cod}")

    except (ConnectionRefusedError, socket.timeout, OSError):
        print("Serverul SMTP este offline!")
        print("Verifica daca server.py este pornit.")

    except smtplib.SMTPException as eroare:
        print(f"Eroare SMTP: {eroare}")
