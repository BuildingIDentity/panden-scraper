import requests

def fetch(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "nl-NL,nl;q=0.9,en;q=0.8",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Connection": "keep-alive"
    }

    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code != 200:
            print(f"Fout {r.status_code} bij {url}")
            return None
        return r.text
    except Exception as e:
        print(f"Request fout bij {url}: {e}")
        return None
