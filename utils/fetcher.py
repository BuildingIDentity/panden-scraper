import requests

def fetch(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) "
            "Gecko/20100101 Firefox/117.0"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "nl,en-US;q=0.7,en;q=0.3",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
    }

    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code != 200:
            print(f"Fout {r.status_code} bij {url}")
            return None
        return r.text
    except Exception as e:
        print(f"Request fout bij {url}: {e}")
        return None
