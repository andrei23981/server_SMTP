
from pathlib import Path
from email import policy
from email.parser import BytesParser
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def citeste_emailuri():
    folder = Path("inbox")
    emailuri = sorted(folder.glob("*.txt"), reverse=True)

    if not emailuri:
        console.print("[yellow]Inbox-ul este gol.[/]")
        return

    # Tabelul cu emailuri
    tabel = Table(title="INBOX", border_style="cyan")
    tabel.add_column("Nr.", style="cyan")
    tabel.add_column("Expeditor", style="green")
    tabel.add_column("Subiect", style="white")

    mesaje = []

    for index, fisier in enumerate(emailuri, start=1):
        continut_fisier = fisier.read_bytes()
        # Mesajele salvate anterior cu write_text pe Windows au CR dublu.
        continut_fisier = continut_fisier.replace(b"\r\r\n", b"\r\n")
        mesaj = BytesParser(policy=policy.default).parsebytes(
            continut_fisier
        )
        mesaje.append(mesaj)

        tabel.add_row(
            str(index),
            str(mesaj["From"] or "Necunoscut"),
            str(mesaj["Subject"] or "Fara subiect")
        )

    console.print(tabel)

    alegere = input("\nAlege numarul emailului: ").strip()

    if not alegere.isdigit() or not 1 <= int(alegere) <= len(mesaje):
        console.print("[red]Email invalid![/]")
        return

    mesaj = mesaje[int(alegere) - 1]

    continut = mesaj.get_body(preferencelist=("plain",))
    text = continut.get_content() if continut else "(Fara continut)"

    detalii = (
        f"[cyan]De la:[/] {mesaj['From']}\n"
        f"[cyan]Catre:[/] {mesaj['To']}\n"
        f"[cyan]Subiect:[/] {mesaj['Subject']}\n"
    )

    console.print(
        Panel(
            detalii,
            title="EMAIL SELECTAT",
            border_style="green",
            expand=False
        )
    )

    console.print(
        Panel(
            text,
            title="Mesaj",
            border_style="cyan",
            expand=False
        )
    )
