# SMTP Email System — Andrei & Mario

Proiect pentru **Unit 03: Designing a Simple Cryptocurrency — Task 1: SMTP Server**.

**Scop:** Andrei și Mario pornesc fiecare câte un server SMTP pe propriul laptop Windows, trimit mesaje în ambele direcții și le citesc din terminal. Pentru conexiunea la distanță folosesc Tailscale, cu **două conturi diferite**.

## 1. Pregătire (amândoi)

1. Instalați Python și Tailscale pe Windows.
2. Copiați același proiect pe fiecare laptop (`server.py`, `client.py`, `main.py`, `inbox.py`, `connection.py`, `config.py`).
3. În PowerShell, din folderul proiectului, instalați dependențele:

   ```powershell
   python -m pip install aiosmtpd rich
   ```

4. Fiecare se autentifică în Tailscale cu **propriul cont**.

## 2. Conectarea conturilor Tailscale

Pentru că sunt conturi diferite, trebuie permis accesul în ambele direcții:

1. Andrei deschide [Tailscale Admin — Machines](https://login.tailscale.com/admin/machines), selectează laptopul lui și alege **Share**. Trimite invitația lui Mario.
2. Mario acceptă invitația.
3. Mario face **Share** pentru laptopul său către Andrei.
4. Andrei acceptă invitația.

Partajarea reciprocă contează: un dispozitiv partajat este restricționat implicit în privința inițierii conexiunilor către rețeaua celuilalt. [Documentația Tailscale](https://tailscale.com/docs/features/sharing).

Pe fiecare laptop, în PowerShell:

```powershell
tailscale ip -4
```

Notați IP-urile afișate și verificați că fiecare poate vedea dispozitivul celuilalt în Tailscale.

## 3. Configurarea `config.py`

**Laptop Andrei:**

```python
EMAIL = "andrei@test.local"
SERVER_HOST = "IP_TAILSCALE_ANDREI"
SERVER_PORT = 1025
DESTINATION_HOST = "IP_TAILSCALE_MARIO"
DESTINATION_PORT = 1025
```

**Laptop Mario:**

```python
EMAIL = "mario@test.local"
SERVER_HOST = "IP_TAILSCALE_MARIO"
SERVER_PORT = 1025
DESTINATION_HOST = "IP_TAILSCALE_ANDREI"
DESTINATION_PORT = 1025
```

Înlocuiți textele `IP_TAILSCALE_...` cu **IP-urile reale** (de forma `100.x.y.z`), fără să păstrați paranteze sau alte caractere. `SERVER_HOST` este IP-ul *propriului* laptop; `DESTINATION_HOST` este IP-ul *celuilalt* laptop. Nu puneți IP-ul partenerului în `SERVER_HOST`.

Verificați că proiectul folosește variabilele din `config.py`:

- În `server.py`, `Controller(..., hostname=SERVER_HOST, port=SERVER_PORT)`; funcția `handle_RCPT` acceptă doar `EMAIL` al acelui laptop.
- În `client.py`, antetul `From` folosește `EMAIL`, iar `smtplib.SMTP(DESTINATION_HOST, DESTINATION_PORT, timeout=5)` se conectează la partener.

**Important:** `aiosmtpd` poate da `WinError 10049` la pornire dacă IP-ul setat nu există pe laptop. Pentru test local, folosiți `SERVER_HOST = "127.0.0.1"`; pentru schimbul la distanță, reveniți la IP-ul Tailscale propriu.

## 4. Firewall și testarea conexiunii

Pe fiecare laptop permiteți **intrarea TCP pe portul 1025 numai de la IP-ul Tailscale al partenerului**, prin Windows Defender Firewall. Nu deschideți portul către internetul public. Dacă nu funcționează, verificați și permisiunile de acces Tailscale.

Porniți serverul pe ambele laptopuri, fiecare într-un terminal PowerShell:

```powershell
python server.py
```

Într-un alt terminal, de pe laptopul Andrei:

```powershell
Test-NetConnection IP_TAILSCALE_MARIO -Port 1025
```

De pe laptopul Mario:

```powershell
Test-NetConnection IP_TAILSCALE_ANDREI -Port 1025
```

Înlocuiți IP-urile placeholder cu cele reale. **`TcpTestSucceeded : True`** indică faptul că portul SMTP poate fi accesat.

## 5. Demonstrația SMTP (amândoi)

Cu `server.py` pornit pe ambele laptopuri, deschideți un al doilea terminal pe fiecare și rulați:

```powershell
python main.py
```

1. **Andrei:** alege `1. Trimite un email` și trimite către `mario@test.local`.
2. **Mario:** alege `2. Vezi emailurile primite`, selectează mesajul și îl citește.
3. **Mario:** trimite un email către `andrei@test.local`.
4. **Andrei:** deschide inboxul și citește răspunsul.

Mesajele sunt salvate local în folderul `inbox/` al serverului **destinatarului**, nu al expeditorului. Adresele `@test.local` sunt identificatori de laborator, nu căsuțe Gmail sau Yahoo.

## 6. Predarea

- Comunicați numele partenerului în **comentariul privat** al temei.
- Înregistrați un singur videoclip cu o scurtă explicație a configurării, ambele servere pornite, trimiterea și citirea mesajului la Mario, apoi răspunsul și citirea lui la Andrei.
- Faceți totul din **terminal**, fără aplicații grafice pentru trimiterea și citirea emailurilor (interfața Rich din terminal este permisă).
- Încărcați videoclipul **o singură dată**, înainte de **10 noiembrie**.

## Probleme frecvente

| Problemă | Verificare |
|---|---|
| `WinError 10049` | `SERVER_HOST` trebuie să fie IP-ul existent pe laptopul propriu. |
| `Connection refused` | Serverul destinatar este pornit? Portul `1025` este corect? |
| `TcpTestSucceeded : False` | Verificați partajarea reciprocă Tailscale, IP-ul și firewall-ul Windows. |
| `550 Destinatar necunoscut` | Adresa `To` trebuie să corespundă variabilei `EMAIL` de pe serverul destinatar. |
| Mesajul apare în inboxul greșit | Verificați `DESTINATION_HOST` și adresa destinatarului. |

**Notă de securitate:** Acest server de laborator nu implementează autentificare SMTP sau TLS în Python. Folosiți-l numai în rețeaua privată Tailscale, cu acces restricționat la cele două dispozitive.
