
import os

from client import trimite_email
from inbox import citeste_emailuri
from connection import verifica_conexiunea



from rich.console import Console
from rich.panel import Panel

console = Console()

def afisare_meniu():
    meniu = """
[bold cyan]1.[/] Trimite un email
[bold cyan]2.[/] Vezi emailurile primite
[bold cyan]3.[/] Verifica serverul SMTP
[bold cyan]4.[/] Iesire
"""

    console.print(
        Panel(
            meniu,
            title="[bold green]SMTP EMAIL SYSTEM[/]",
            border_style="cyan",
            expand=False
        )
    )



def main():
    while True:
        os.system("cls")
        afisare_meniu()

        optiune = input("\nAlege o optiune [1..4]: ").strip()

        os.system("cls")

        if optiune == "1":
            trimite_email()

        elif optiune == "2":
            citeste_emailuri()

        elif optiune == "3":
            verifica_conexiunea()

        elif optiune == "4":
            print("Ne auzim!!! 😊")
            break

        else:
            print("Optiune invalida!")

        input("\nApasa ENTER pentru a reveni la meniu...")


if __name__ == "__main__":
    main()
