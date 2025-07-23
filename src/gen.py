from captcha import solve
import requests
import random
import string
import threading

def generate_account_exp(account_id):
    def random_string(n):
        return ''.join(random.choice(string.ascii_letters) for _ in range(n))


# Payload
# {"user_account":{"first_name":"Tigran","last_name":"Sev","is_teacher":null,"birthday":"2004-09-03","locale_code":"en-GB","email":"ewgfwng@dca.net","password":"rizz123456"},"marketing_email_preference":true,"utm_tags":{}}


    headers = {
  "accept": "application/json, text/plain, */*",
  "accept-encoding": "gzip, deflate, br, zstd",
  "accept-language": "en-US,en;q=0.9,nl;q=0.8",
  "cache-control": "no-cache",
  "content-length": "68",
  "content-type": "application/json",
  "origin": "https://studygo.com",
  "pragma": "no-cache",
  "priority": "u=1, i",
  "referer": "https://studygo.com/",
  "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
  "sec-ch-ua-mobile": "?0",
  "sec-ch-ua-platform": "\"Windows\"",
  "sec-fetch-dest": "empty",
  "sec-fetch-mode": "cors",
  "sec-fetch-site": "cross-site",
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
  "x-client-type": "web",
  "x-device-id": "a46e6264-9f44-47e7-8c0c-c639af757a84",
  "x-language-code": "nl",
  "x-locale-code": "nl-NL",
  "x-session-id": "1e63d6ec-fa87-4b5b-816d-c08cbb091de6"
}

    cap = solve(
    url="https://studygo.com/en/learn/sign-up/",
    key="6Le57PIbAAAAANlypH1E_aSAYL2V-j3l1IFiNM9Y",
    client_key="armenië")
    if cap == None:
        print("[X] Captcha key invalid, stopping")
        return


# Account info
    nederlandse_voornamen = ["Jan", "Pieter", "Kees", "Henk", "Jeroen", "Mark", "Sander", "Willem", "Bas", "Tim", "Tigran"]
    nederlandse_achternamen = ["de Jong", "Jansen", "de Vries", "van den Berg", "van Dijk", "Bakker", "Asatryan"]

    voornaam = random.choice(nederlandse_voornamen)
    achternaam = random.choice(nederlandse_achternamen)

    email = f"{random_string(6)}@dca.net"
    password = random_string(8)

    payload = {
    "user_account":
    {
        "first_name":voornaam,
        "last_name":achternaam,
        "is_teacher": None,
        "birthday":f"{str(random.randint(2002, 2008))}-{str(random.randint(1, 11))}-{str(random.randint(1, 11))}",
        "locale_code":"en-GB",
        "email": email,
        "password": password
    },
        "marketing_email_preference":True,
        "utm_tags": {},
        "recaptcha_token": cap
}

    res = requests.post(headers=headers, url="https://api.wrts.nl/api/v3/public/user_accounts", json=payload)
    if res.status_code != 200:
        if res.json() == {'errors': [{'attribute': 'recaptcha_token', 'message': 'Captcha was niet geaccepteerd, probeer het nog een keer'}]}:
            print("[!] Captcha was not accepted. Retrying... | ID: " + str(account_id))
            generate_account_exp(403)

        print(f"[X] Account creation failed;\n{res.json()}")
        return
    
    with open("accounts.txt", "a") as f:
        f.write(f"{email}:{password}\n")
    print(f"[V] Account generated | ID: {account_id}")
    return f"{email}:{password}"


import threading


def generate_accounts(n):
    threads = []
    for i in range(1, n + 1):
        t = threading.Thread(target=generate_account_exp, args=(i,))
        t.start()
        # print(f"Started generation thread for account ID: {i}")
        threads.append(t)

    for t in threads:
        t.join()

if __name__ == '__main__':
    # Example usage
    while True:
        amount = int(input("Enter amount of accounts to be generated\n> "))
        generate_accounts(amount)
        print(f"{amount} accounts generated.")
        print("------------")