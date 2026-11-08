from aiosmtpd.controller import Controller
from pathlib import Path
from datetime import datetime
from config import EMAIL, SERVER_HOST, SERVER_PORT

class EmailHandler:
    async def handle_DATA(self, server, session, envelope):
        print("Am primit un email")
        mesaj = envelope.content.decode('utf8', errors='replace')
        folder = Path("inbox")
        folder.mkdir(exist_ok=True)
        nume = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        fisier = folder / f"{nume}.txt"
        fisier.write_text(mesaj, encoding='utf8')
        print(f"Email salvat in fisierul: {fisier}")
        return "250 OK"

    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        if address.lower() != EMAIL.lower():
            return "550 Destinatar necunoscut"

        envelope.rcpt_tos.append(address)
        return "250 OK"

controller = Controller(
    EmailHandler(),
    hostname=SERVER_HOST,
    port=SERVER_PORT
)

controller.start()
print("Serverul SMPT a pornit pe portul 1025")

try:
    input("Apasa Enter pentru a opri serverul...\n")
finally:
    controller.stop()
    print("Serverul SMTP a fost oprit.")