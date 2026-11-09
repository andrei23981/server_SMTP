# Server SMTP — trimitere de emailuri între doi colegi

Fiecare coleg pornește serverul pe propriul laptop Windows. Mesajele se trimit prin Tailscale și se citesc din terminal; adresele `@test.local` sunt doar pentru acest proiect, nu sunt adrese de internet.

## 1. Pregătire (pe ambele laptopuri)

1. Instalați Python și Tailscale. Copiați proiectul pe ambele laptopuri.
2. În PowerShell, din folderul proiectului, instalați dependențele:

   ```powershell
   python -m pip install aiosmtpd rich
   ```

3. Conectați-vă la Tailscale. Dacă aveți conturi diferite, mergeți la [Tailscale Admin — Machines](https://login.tailscale.com/admin/machines): Andrei selectează laptopul lui și apasă **Share** către Mario, iar Mario acceptă invitația. Apoi Mario face **Share** pentru laptopul lui către Andrei, iar Andrei acceptă.
4. Fiecare își află IP-ul Tailscale cu `tailscale ip -4` și îl comunică celuilalt.

## 2. Configurați `config.py` pe fiecare laptop

Înlocuiți `IP_TAILSCALE_ANDREI` și `IP_TAILSCALE_MARIO` cu IP-urile Tailscale reale (de forma `100.x.y.z`). `SERVER_HOST` este **IP-ul propriului laptop**, iar `DESTINATION_HOST` este **IP-ul celuilalt**.

**Laptopul lui Andrei:**

```python
EMAIL = "andrei@test.local"
SERVER_HOST = "IP_TAILSCALE_ANDREI"
SERVER_PORT = 1025
DESTINATION_HOST = "IP_TAILSCALE_MARIO"
DESTINATION_PORT = 1025
```

**Laptopul lui Mario:**

```python
EMAIL = "mario@test.local"
SERVER_HOST = "IP_TAILSCALE_MARIO"
SERVER_PORT = 1025
DESTINATION_HOST = "IP_TAILSCALE_ANDREI"
DESTINATION_PORT = 1025
```

## 3. Permiteți conexiunea și porniți serverele

Pe **fiecare laptop**, permiteți în Windows Firewall conexiunile TCP la portul `1025` doar de la IP-ul Tailscale al celuilalt. De exemplu, în **PowerShell ca administrator**:

```powershell
New-NetFirewallRule -DisplayName "SMTP tema" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 1025 -RemoteAddress IP_CELUILALT
```

Înlocuiți `IP_CELUILALT` cu IP-ul real al partenerului. Nu deschideți portul către internetul public.

Pe ambele laptopuri, în folderul proiectului, porniți serverul și lăsați terminalul deschis:

```powershell
python server.py
```

## 4. Trimiteți și citiți mesajele

Deschideți **un al doilea terminal** pe fiecare laptop, în același folder:

```powershell
python main.py
```

1. Andrei alege `1` și trimite către `mario@test.local`.
2. Mario alege `2` și citește mesajul.
3. Mario alege `1` și trimite către `andrei@test.local`.
4. Andrei alege `2` și citește răspunsul.

Dacă nu merge, verificați că **ambele servere sunt pornite**, IP-urile din `config.py` sunt corecte, invitațiile Tailscale sunt acceptate și firewall-ul permite portul `1025`. Puteți testa conexiunea din meniu cu opțiunea `3`. Mesajele primite se salvează în folderul local `inbox/`.

**Securitate:** Serverul nu are autentificare sau TLS; folosiți-l doar prin Tailscale, între cele două laptopuri.
