import requests
import time
import random

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        " AppleWebKit/537.36 (KHTML, like Gecko)"
        " Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "nl-BE,nl;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
    "Connection": "keep-alive"
}

def fetch(url, tries=3):
    for attempt in range(tries):
        try:
            time.sleep(random.uniform(0.5, 1.2))
            r = requests.get(url, headers=HEADERS, timeout=15)
            if r.status_code == 200:
                return r.text
            else:
                print(f"[fetch] status {r.status_code} bij {url}")
        except Exception as e:
            print(f"[fetch] error: {e}")

        print("[fetch] retry…")
        time.sleep(1 + attempt * 1.5)

    return None
