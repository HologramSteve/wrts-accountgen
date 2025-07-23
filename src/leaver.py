from captcha import solve
import requests
import threading

def leave(token, groupId):
    def post(url: str, payload, headers):
        if not url[0] == "/":
            return "Please enter a valid field!"
        response = requests.post(f"https://api.wrts.nl/api/v3{url}", json=payload, headers=headers)
        return response

    if token.strip() == "":
        return 2


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
    email = token.split(":")[0]
    password = token.split(":")[1]
    res = post("/auth/get_token", payload={"email": email, "password": password}, headers=headers)
    resjson = res.json()
    if resjson == {'errors': [{'attribute': 'recaptcha_token', 'message': 'Los eerst de captcha op'}]}:
        # print(f"[!] Account captcha-locked, attempting solve...")
        captcha_token = solve(
        url="https://studygo.com/en/learn/sign-in/",
        key="6Le57PIbAAAAANlypH1E_aSAYL2V-j3l1IFiNM9Y",
        client_key="sev achker"
    )
        res = post("/auth/get_token", payload={"email": email, "password": password, "recaptcha_token": captcha_token}, headers=headers)
    try:
        headers["X-Auth-Token"] = res.json()["auth_token"]
    except KeyError:
        print(f"TOKEN: {token} | RESULT: ERROR (invalid credentials)")
        return 0
    
    res = requests.delete(f"https://api.wrts.nl/api/v3/groups/{groupId}/leave_group", json={}, headers=headers)

    print(f"TOKEN: {token} | RESULT: LEFT")
    return 1

def massleave(credentials, groupId):
    print(f"Leaving with {len(credentials)} tokens...")
    valid = 0
    invalid = 0
    invalidtype = 0
    results = [None] * len(credentials)
    threads = []

    def worker(index, token):
        result = leave(token, groupId)
        results[index] = result

    for i, token in enumerate(credentials):
        thread = threading.Thread(target=worker, args=(i, token))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.leave()

    for result in results:
        if result == 0:
            invalid += 1
        elif result == 1:
            valid += 1
        elif result == 2:
            invalidtype += 1

    print(f"RESULTS\n-------------------------\nValid: {valid}\nInvalid: {invalid}\nInvalid (syntax): {invalidtype}\nTotal: {len(credentials)}")

with open("accounts.txt", 'r') as f:
    data = f.read()
    tokens = data.split("\n")

while True:
    groupid = input("Enter group ID\n> ")
    massleave(tokens, groupid)