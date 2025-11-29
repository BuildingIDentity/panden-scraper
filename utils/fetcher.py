import requests
import time
import random

def fetch(url):
    headers = {
        "User-Agent": random.choice([
            "Mozilla/5.0",
            "Mozilla/5.0 (Windows NT 10.0)",
            "Mozilla/5.0 (Macintosh)",
        ])
    }
    
    time.sleep(random.uniform(0.5, 2.0))
    
    r = requests.get(url, headers=headers, timeout=15)
    if r.status_code != 200:
        print(f"Fout {r.status_code} bij {url}")
        return None
    
    return r.text

