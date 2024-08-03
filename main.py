import os, sys, json, time, random, string, ctypes, logging
import threading
import concurrent.futures

try:
    import requests
    import colorama
    import pystyle
    import datetime
    import capmonster_python
except ModuleNotFoundError:
    os.system("pip install requests colorama pystyle datetime capmonster_python")

from colorama import Fore, Style
from tls_client import Session
from random import choice
from json import dumps
from pystyle import System, Colors, Colorate, Write
from capmonster_python import HCaptchaTask
from concurrent import futures
from threading import Lock

red = Fore.RED
yellow = Fore.YELLOW
green = Fore.GREEN
blue = Fore.BLUE
orange = Fore.RED + Fore.YELLOW
pretty = Fore.LIGHTMAGENTA_EX + Fore.LIGHTCYAN_EX
magenta = Fore.MAGENTA
lightblue = Fore.LIGHTBLUE_EX
cyan = Fore.CYAN
gray = Fore.LIGHTBLACK_EX + Fore.WHITE
reset = Fore.RESET
pink = Fore.LIGHTGREEN_EX + Fore.LIGHTMAGENTA_EX
dark_green = Fore.GREEN + Style.BRIGHT

joined = 0
solved = 0
errors = 0
rules = 0

tokens = []

def update_console_title():
    ctypes.windll.kernel32.SetConsoleTitleW(f'Discord Token Joiner | Joined : {joined} | Solved : {solved} | Errors : {errors} | Accepted Rules : {rules} | Total Tokens : {len(tokens)}')

def get_time_rn():
    date = datetime.datetime.now()
    return date.strftime("%H:%M:%S")

def ui():
    Write.Print("""
\t ▄▀▀▀█▀▀▄  ▄▀▀▀▀▄   ▄▀▀▄ █  ▄▀▀█▄▄▄▄  ▄▀▀▄ ▀▄            ▄█  ▄▀▀▀▀▄   ▄▀▀█▀▄    ▄▀▀▄ ▀▄  ▄▀▀█▄▄▄▄  ▄▀▀▄▀▀▀▄ 
\t█    █  ▐ █      █ █  █ ▄▀ ▐  ▄▀   ▐ █  █ █ █      ▄▀▀▀█▀ ▐ █      █ █   █  █  █  █ █ █ ▐  ▄▀   ▐ █   █   █ 
\t▐   █     █      █ ▐  █▀▄    █▄▄▄▄▄  ▐  █  ▀█     █    █    █      █ ▐   █  ▐  ▐  █  ▀█   █▄▄▄▄▄  ▐  █▀▀█▀  
\t   █      ▀▄    ▄▀   █   █   █    ▌    █   █      ▐    █    ▀▄    ▄▀     █       █   █    █    ▌   ▄▀    █  
\t ▄▀         ▀▀▀▀   ▄▀   █   ▄▀▄▄▄▄   ▄▀   █         ▄   ▀▄    ▀▀▀▀    ▄▀▀▀▀▀▄  ▄▀   █    ▄▀▄▄▄▄   █     █   
\t█                  █    ▐   █    ▐   █    ▐          ▀▀▀▀            █       █ █    ▐    █    ▐   ▐     ▐   
\t▐                  ▐        ▐        ▐                               ▐       ▐ ▐         ▐                  
""", Colors.green_to_white, interval=0.0000)

def generate_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=59))

def generate_tokens(stop_event):
    while not stop_event.is_set():
        tokens.append(generate_token())
        update_console_title()
        time.sleep(0.0005)

def captcha_bypass(token, url, key, captcha_rqdata):
    global solved
    with open("config.json") as dsc_ez:
        config = json.load(dsc_ez)
        startedSolving = time.time()
        capmonster = HCaptchaTask(config['capmonster_key'])
        task_id = capmonster.create_task(url, key, is_invisible=True, custom_data=captcha_rqdata)
        result = capmonster.join_task_result(task_id)
        response = result.get("gRecaptchaResponse")
        time_rn = get_time_rn()
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({yellow}*{gray}) {pretty}Solved {gray}|{pink} {yellow}{response[-32:]} {gray}In {yellow}{round(time.time()-startedSolving)}s")
        solved += 1
        update_console_title()
        return response

def nonce():
    date = datetime.datetime.now()
    unixts = time.mktime(date.timetuple())
    return str((int(unixts)*1000-1420070400000)*4194304)

def join(token, invite_code):
    global joined, solved, errors, rules
    proxy = choice(open("proxies.txt", "r").readlines()).strip() if len(open("proxies.txt", "r").readlines()) != 0 else None

    session = Session(client_identifier="chrome_114", random_tls_extension_order=True)

    if proxy.count(":") == 1:
        session.proxies = {
            "http": "http://" + proxy,
            "https": "http://" + proxy
        }
    elif proxy.count(":") == 3:
        username, password, ip, port = proxy.split(":")
        session.proxies = {
            "http": f"http://{username}:{password}@{ip}:{port}",
            "https": f"http://{username}:{password}@{ip}:{port}"
        }

    headers_finger = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Referer': 'https://discord.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36 Edg/114.0.1823.51',
        'X-Track': 'eyJvcyI6IklPUyIsImJyb3dzZXIiOiJTYWZlIiwic3lzdGVtX2xvY2FsZSI6ImVuLUdCIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKElQaG9uZTsgQ1BVIEludGVybmFsIFByb2R1Y3RzIFN0b3JlLCBhcHBsaWNhdGlvbi8yMDUuMS4xNSAoS0hUTUwpIFZlcnNpb24vMTUuMCBNb2JpbGUvMTVFMjQ4IFNhZmFyaS82MDQuMS4xMiIsImJyb3dzZXJfdmVyc2lvbiI6Ijk5LjAuNDg4MS42OCIsIm9zX3ZlcnNpb24iOiIxNDA0MSIsInJlZmVycmluZ19kb21haW4iOiJnb29nbGUuY29tIiwicmVmZXJyaW5nX2Zyb20iOiJodHRwczovL2NvbnNvbGUuZGV2L2FwaS8ifQ=='
    }

    time_rn = get_time_rn()
    try:
        # Bypass Fingerprint
        fingerprint = session.get("https://discord.com/api/v9/experiments", headers=headers_finger).json()['fingerprint']
        headers_invite = {
            'accept': '*/*',
            'accept-language': 'en-US',
            'authorization': token,
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'referer': 'https://discord.com/channels/@me',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'x-debug-options': 'bugReporterEnabled',
            'x-fingerprint': fingerprint,
            'x-super-properties': 'eyJvcyI6IkxpbnV4IiwicmVsZWFzZV9jaGFubmVsIjoid2ViIiwiYnJvd3NlciI6IkNocm9tZSIsImJyb3dzZXJfdmVyc2lvbiI6IjEwNC4wLjUxMTIuMTE0IiwiZGV2aWNlX3ZlbmRvciI6Ikdvb2dsZSBJbmMuIiwidmVyc2lvbiI6IjEwNC4wIiwib3NfdmVyc2lvbiI6IkxpbnV4IDUuMTEuMCIscmVmZXJyaW5nX3JlZ2lvbiI6IkRFLU5PIiwicmVmZXJyaW5nX2RvbWFpbiI6Imdvb2dsZS5jb20iLCJzZXR0aW5ncyI6eyJtaW5vcml0eSI6ZmFsc2UsImZpdF9hc2NyZWVuIjp0cnVlfX0='
        }
        # Bypass Captcha
        r1 = session.post(f"https://discord.com/api/v9/invites/{invite_code}", headers=headers_invite)
        if r1.status_code == 200:
            pass
        elif "captcha_rqdata" in r1.text:
            captcha_rqdata = r1.json()['captcha_rqdata']
            sitekey = r1.json()['captcha_sitekey']
            task = captcha_bypass(token, f"https://discord.com/api/v9/invites/{invite_code}", sitekey, captcha_rqdata)
            payload = {
                "captcha_key": task
            }
            session.post(f"https://discord.com/api/v9/invites/{invite_code}", headers=headers_invite, json=payload)
        else:
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}x{gray}) {pretty}Failed {gray}| {red}{r1.text}{reset}")
            errors += 1
            update_console_title()
            return
        # Bypass Rules
        r2 = session.get("https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots", headers=headers_invite).json()
        if "code" in r2:
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({yellow}*{gray}) {pretty}Joined {gray}| {cyan}{invite_code}{reset}")
            joined += 1
            update_console_title()
        if "SHOW_RULES" in r2:
            rules_payload = {
                "form_fields": r2["show_form_fields"],
                "version": r2["version"],
                "form_type": r2["form_type"]
            }
            session.post(f"https://discord.com/api/v9/guilds/{r2['guild_id']}/requests/@me", headers=headers_invite, json=rules_payload)
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({yellow}*{gray}) {pretty}Accepted Rules {gray}| {cyan}{invite_code}{reset}")
            rules += 1
            update_console_title()
    except Exception as e:
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}x{gray}) {pretty}Error {gray}| {red}{str(e)}{reset}")
        errors += 1
        update_console_title()

def main():
    ui()
    stop_event = threading.Event()
    invite_code = input(f"{gray}[{yellow}?{gray}] Server invite: {cyan}").strip()
    threading.Thread(target=generate_tokens, args=(stop_event,)).start()

    try:
        input(f"{gray}[{yellow}!{gray}] Press Enter to stop generating tokens and start joining...")
    finally:
        stop_event.set()

    with open("tokens.txt", "w") as f:
        for token in tokens:
            f.write(token + "\n")

    print(f"{gray}[{yellow}*{gray}] Generated {len(tokens)} tokens. Starting to join...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for token in tokens:
            executor.submit(join, token, invite_code)

if __name__ == "__main__":
    main()
