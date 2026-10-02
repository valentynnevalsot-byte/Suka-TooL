#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Suka-TooL — testing framework for YOUR OWN infrastructure
# Only use on systems you own or have written permission to test.

import os, sys, time, socket, subprocess, threading, json, shutil, urllib.request, urllib.parse, platform

BANNER = r"""
 ▄▄▄▄▀▀▀▀▀▄     ▄▄▄▄     ▄     ▄▄▀▒     ▄     ▄▄▄▄▀▀▀▀▀▄     ▄▄▄▄▀▀▀▀▀▄    ▄▄▄▄▀▀▀▀▀▄     ▄▄▄▄▀▀▀▀▀▄     ▄▄▄▄
▄▀████▄▄███    ▄▀██▒     ░▀▄  ▄▀██░     ░▀▄  ▄▀████▄▄██▀▀▄  ▄▀████▄▄██▀▀▄ ▄▀████▄▄██▀▀▄  ▄▀████▄▄██▀▀▄  ▄▀██▒
▓███▓▀▀▀▄▄▄▄▄  ▓███░     ▒██▄ ▓████    ▄▒██▄ ▓███▄▄▀▀▄▄███▄ ▓███▄▄▀▀▄▄███ ▓███▄▄▀▀▄▄███▄ ▓███▄▄▀▀▄▄███▄ ▓███░
▀▀▀▀▀▄▄▄▄▓▓▓▀▀ ▒▓▓▓░     ▓▓▓█ ▒▓▓▓█▄▄▄▀▄▀▓▓█ ▒▓▓▓░ ▄▄▄▀█▓▓█ ▒▓▓▓░    ▀▀▀▀ ▒▓▓▓░     ░▓▓█ ▒▓▓▓░     ░▓▓█ ▒▓▓▓░
░▀▀▀░   ▀▄▄▒▒▒ ░▒▒▒▒▄    ░▒▒█ ░▒▒▒▄▄▄▄▄▄▓▒▀▀ ░▒▒▒▒ ▒▄▄▄▄▒▒░ ░▒▒▒░         ░▒▒▒▒▄    ▒▒▒█ ░▒▒▒▒▄    ▒▒▒█ ░▒▒▒▒    ▄▄▄▄▄
▀▄▄░ ▀▀▀▄▀▄░░▓ ▀▄▄░ ▀▀▀▄▀▄░░▒ █░░░▓   ▀▄█░░▒ █░░░▓     █░░▒ ▄▄░░▒         ▀▄▄░ ▀▀▀▄▀▄░░▒ ▀▄▄░ ▀▀▀▄▀▄░░▒ ▄▄░░ ▀▀▄▀▀ ░░▒
  ▀▀▄▄▄▄▄▄▄▄▀    ▀▀▄▄▄▄▄▄▄▄▀  █▄▄▄█     █▄▄▓ █▄▄▄█     █▄▄▓  ▀▄▄▓           ▀▀▄▄▄▄▄▄▄▄▀    ▀▀▄▄▄▄▄▄▄▄▀   ▀▄▄▄▄▄▄▄▄▄▄▀
"""

EXIT_ART = r"""
     _     _      _               _        _
    /\ \ /_/\    /\ \            /\ \     /\ \
   /  \ \\ \ \   \ \_\           \ \ \    \_\ \
  / /\ \ \\ \ \__/ / /           /\ \_\   /\__ \
 / / /\ \_\\ \__ \/_/           / /\/_/  / /_ \ \
/ /_/_ \/_/ \/_/\__/\          / / /    / / /\ \ \
/ /____/\     _/\/__\ \        / / /    / / /  \/_/
/ /\____\/    / _/_/\ \ \      / / /    / / /
/ / /______   / / /   \ \ \ ___/ / /__  / / /
/ / /_______\ / / /    /_/ //\__\/_/___\/_/ /
\/__________/ \/_/     \_\/ \/_________/\_\//
"""

CY = "\033[96m"; GR = "\033[92m"; YL = "\033[93m"; RD = "\033[91m"; RS = "\033[0m"

if not (sys.stdout.isatty() and os.environ.get("TERM") != "dumb"):
    CY = GR = YL = RD = RS = ""

def _clear():
    os.system("cls" if os.name == "nt" else "clear")

def _width():
    return shutil.get_terminal_size((80, 24)).columns

def show_banner():
    print(CY + BANNER + RS)

# ---------- loading ----------
def loading():
    show_banner()
    bar_len = 40
    for i in range(bar_len + 1):
        pct = int(i / bar_len * 100)
        bar = "█" * i + "░" * (bar_len - i)
        sys.stdout.write(f"\r  [{bar}] {pct}%")
        sys.stdout.flush()
        time.sleep(0.03)
    print(GR + "\n  [OK] Ready." + RS + "\n")
    time.sleep(0.3)

def menu():
    print(YL + "  ┌──────────────────────────────────────────────────────┐")
    print(YL + "  │" + GR + " S U K A  -  T O O L   M A I N   M E N U ".center(54) + YL + "│")
    print(YL + "  ├──────────────────────────────────────────────────────┤")
    items = [
        ("1",  "IP lookup (geolocation / ISP)"),
        ("2",  "Port scanner (1-1024)"),
        ("3",  "Stress test (OWN server only)"),
        ("4",  "WiFi scan (nearby networks)"),
        ("5",  "WiFi passwords (this machine)"),
        ("6",  "Web recon (security headers)"),
        ("7",  "Webcam capture (local)"),
        ("8",  "Username tracer"),
        ("9",  "Phone number info"),
        ("10", "OSINT dashboard"),
        ("11", "Update tool"),
        ("12", "Exit"),
    ]
    for num, label in items:
        print(YL + "  │ " + CY + f"[{num:>2}] " + GR + f"{label:<48}" + YL + " │")
    print(YL + "  └──────────────────────────────────────────────────────┘")

def ask(prompt):
    return input(CY + "\n  >> " + prompt + ": " + RS).strip()

# ---------- 1. IP lookup ----------
def ip_lookup():
    ip = ask("IP address or domain")
    try:
        target = socket.gethostbyname(ip)
        data = json.loads(urllib.request.urlopen(
            f"http://ip-api.com/json/{target}", timeout=10).read().decode())
        if data.get("status") != "success":
            print(RD + "  Lookup failed." + RS); return
        print(GR + f"""
  IP        : {target}
  Country   : {data.get('country')} ({data.get('countryCode')})
  Region    : {data.get('regionName')}
  City      : {data.get('city')}
  ISP       : {data.get('isp')}
  Org       : {data.get('org')}
  AS        : {data.get('as')}""" + RS)
    except Exception as e:
        print(RD + f"  Error: {e}" + RS)

# ---------- 2. Port scanner ----------
def port_scan():
    target = ask("Target (own / authorized host only)")
    try:
        host = socket.gethostbyname(target)
    except socket.gaierror:
        print(RD + "  Invalid domain." + RS); return
    open_ports = []
    lock = threading.Lock()
    def worker(p):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        if s.connect_ex((host, p)) == 0:
            with lock: open_ports.append(p)
        s.close()
    print(GR + "  Scanning ports 1-1024..." + RS)
    threads = [threading.Thread(target=worker, args=(p,)) for p in range(1, 1025)]
    for t in threads: t.start()
    for t in threads: t.join()
    if open_ports:
        print(GR + "  Open ports: " + ", ".join(map(str, sorted(open_ports))) + RS)
    else:
        print(RD + "  No open ports in range." + RS)

# ---------- 3. Stress test (own server only) ----------
def stress_test():
    print(YL + "  WARNING: only use on your OWN server!" + RS)
    if ask("Confirm ownership (yes/no)").lower() != "yes":
        print(RD + "  Cancelled." + RS); return
    target = ask("IP:PORT of your server")
    try:
        host, port = target.rsplit(":", 1); port = int(port)
    except ValueError:
        print(RD + "  Format: 192.168.1.10:80" + RS); return
    dur = int(ask("Duration in seconds"))
    threads_n = int(ask("Thread count"))
    print(GR + f"  Stress testing {host}:{port} for {dur}s..." + RS)
    end_t = time.time() + dur
    sent = [0]; lock = threading.Lock()
    def worker():
        while time.time() < end_t:
            try:
                s = socket.socket(); s.settimeout(1)
                s.connect((host, port)); s.send(b"GET / HTTP/1.1\r\n\r\n")
                s.close()
                with lock: sent[0] += 1
            except Exception:
                pass
    ts = [threading.Thread(target=worker, daemon=True) for _ in range(threads_n)]
    for t in ts: t.start()
    while time.time() < end_t:
        time.sleep(2)
        sys.stdout.write(f"\r  Requests sent: {sent[0]}   ")
        sys.stdout.flush()
    print(GR + f"\n  Done. Total requests: {sent[0]}" + RS)

# ---------- 4. WiFi scan nearby ----------
def wifi_scan():
    print(GR + "  Scanning nearby networks..." + RS)
    try:
        if platform.system() == "Windows":
            print(subprocess.check_output(
                ["netsh", "wlan", "show", "networks", "mode=bssid"]).decode(errors="ignore"))
        else:
            out = subprocess.check_output(
                ["nmcli", "-t", "-f", "SSID,CHAN,SIGNAL,SECURITY", "dev", "wifi"]).decode(errors="ignore")
            for line in out.strip().split("\n"):
                ssid, ch, sig, sec = line.split(":")
                print(f"  SSID: {ssid:<30} ch:{ch:<4} signal:{sig}%  sec:{sec}")
    except Exception as e:
        print(RD + f"  Error (run as admin/root): {e}" + RS)

# ---------- 5. WiFi passwords on this machine ----------
def wifi_passwords():
    print(GR + "  WiFi passwords stored on THIS machine:" + RS)
    try:
        if platform.system() == "Windows":
            out = subprocess.check_output(["netsh", "wlan", "show", "profiles"]).decode(errors="ignore")
            profiles = [l.split(":")[1].strip() for l in out.split("\n") if "All User Profile" in l]
            for p in profiles:
                try:
                    key = subprocess.check_output(
                        ["netsh", "wlan", "show", "profile", f"name={p}", "key=clear"]).decode(errors="ignore")
                    pw = [l.split(":")[1].strip() for l in key.split("\n") if "Key Content" in l]
                    print(f"  {p:<30} -> {pw[0] if pw else '(not stored)'}")
                except Exception:
                    pass
        else:
            out = subprocess.check_output(
                ["nmcli", "-s", "-t", "-f", "NAME,PSK", "connection", "show"]).decode(errors="ignore")
            for line in out.strip().split("\n"):
                name, _, pw = line.partition(":")
                print(f"  {name:<30} -> {pw or '(not stored)'}")
    except Exception as e:
        print(RD + f"  Error: {e}" + RS)

# ---------- 6. Web recon ----------
def web_recon():
    url = ask("URL of your website")
    if not url.startswith("http"): url = "https://" + url
    print(GR + "  Analyzing headers..." + RS)
    try:
        resp = urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=10)
        for h, v in resp.headers.items():
            print(f"  {h:<28}: {v}")
        missing = [h for h in ["X-Frame-Options", "Content-Security-Policy",
                   "Strict-Transport-Security", "X-Content-Type-Options"] if h not in resp.headers]
        if missing:
            print(RD + "  Missing security headers: " + ", ".join(missing) + RS)
        else:
            print(GR + "  All basic security headers present." + RS)
    except Exception as e:
        print(RD + f"  Error: {e}" + RS)

# ---------- 7. Local webcam capture ----------
def own_cam():
    print(GR + "  Capturing snapshot from LOCAL webcam (saved as cam.jpg)" + RS)
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        time.sleep(0.5)
        ret, frame = cap.read(); cap.release()
        if ret:
            cv2.imwrite("cam.jpg", frame)
            print(GR + "  Saved -> cam.jpg" + RS)
        else:
            print(RD + "  Camera unavailable." + RS)
    except ImportError:
        print(RD + "  Install: pip install opencv-python" + RS)

# ---------- 8. Username tracer ----------
def username_tracer():
    user = ask("Username")
    sites = {
        "GitHub":    f"https://github.com/{user}",
        "Twitter/X": f"https://x.com/{user}",
        "Instagram": f"https://instagram.com/{user}",
        "Reddit":    f"https://reddit.com/user/{user}",
        "TikTok":    f"https://tiktok.com/@{user}",
        "Steam":     f"https://steamcommunity.com/id/{user}",
        "YouTube":   f"https://youtube.com/@{user}",
        "Twitch":    f"https://twitch.tv/{user}",
    }
    for name, url in sites.items():
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            code = urllib.request.urlopen(req, timeout=8).getcode()
            mark = GR + "[+]" if code == 200 else YL + "[?]"
            print(f"  {mark} {name:<12} {url}" + RS)
        except Exception:
            print(f"  {RD}[-] {name:<12} {url}" + RS)

# ---------- 9. Phone number info ----------
def phone_info():
    try:
        import phonenumbers
        from phonenumbers import geocoder, carrier, timezone
    except ImportError:
        print(RD + "  Install: pip install phonenumbers" + RS); return
    num = ask("Phone number (international format, +1...)").replace(" ", "")
    try:
        p = phonenumbers.parse(num)
        if not phonenumbers.is_valid_number(p):
            print(RD + "  Invalid number." + RS); return
        print(GR + f"""
  Format     : {phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}
  Country    : {phonenumbers.region_code_for_number(p)}
  Timezones  : {timezone.time_zones_for_number(p)}
  Carrier    : {carrier.name_for_number(p, 'en') or 'unknown'}
  Region     : {geocoder.description_for_number(p, 'en') or 'unknown'}""" + RS)
    except Exception as e:
        print(RD + f"  Error: {e}" + RS)

# ---------- 10. OSINT dashboard ----------
def osint_dashboard():
    q = urllib.parse.quote(ask("Search term (name / domain / email)"))
    links = {
        "Google":         f"https://www.google.com/search?q={q}",
        "HaveIBeenPwned": f"https://haveibeenpwned.com/unifiedsearch/{q}" if "@" in q else None,
        "Shodan":         f"https://www.shodan.io/search?query={q}",
        "Censys":         f"https://search.censys.io/search?resource=hosts&q={q}",
        "WHOIS":          f"https://who.is/whois/{q}",
        "SecurityTrails": f"https://securitytrails.com/domain/{q}/dns",
        "IntelX":         f"https://intelx.io/?s={q}",
    }
    for name, url in links.items():
        if url: print(f"  [>] {name:<16} {url}")

# ---------- 11. Update ----------
def update_tool():
    print(GR + "  Updating..." + RS)
    for pkg in ["phonenumbers", "opencv-python", "requests"]:
        os.system(f"{sys.executable} -m pip install -U {pkg} -q")
    print(GR + "  Done." + RS)

# ---------- exit screen ----------
def exit_screen():
    _clear()
    print(CY + EXIT_ART + RS)
    print(GR + "\n" + "BAY my good boy".center(_width()) + "\n" + RS)
    time.sleep(1.2)

def main():
    _clear()
    loading()
    while True:
        _clear()
        show_banner()   # <-- banner is ALWAYS above the menu
        menu()
        try:
            choice = input(CY + "\n  Suka-TooL > " + RS).strip().lower()
        except (KeyboardInterrupt, EOFError):
            choice = "12"
        actions = {
            "1": ip_lookup, "2": port_scan, "3": stress_test,
            "4": wifi_scan, "5": wifi_passwords, "6": web_recon,
            "7": own_cam, "8": username_tracer, "9": phone_info,
            "10": osint_dashboard, "11": update_tool,
        }
        if choice in ("12", "exit", "quit", "q"):
            exit_screen(); break
        fn = actions.get(choice)
        if fn: fn()
        else: print(RD + "  Invalid choice." + RS)
        input(CY + "\n  [Press Enter to return to menu]" + RS)

if __name__ == "__main__":
    main()
