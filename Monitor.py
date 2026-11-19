import requests
import time
from datetime import datetime


websites = [
    "https://google.com",
    "https://github.com",
]

def check_website(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    print("Website Uptime Monitor started...\n")
    while True:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking...")
        for site in websites:
            status = "UP ✅" if check_website(site) else "DOWN ❌"
            print(f"  {site} → {status}")
        print("-" * 40)
        time.sleep(60)  # check every 60 seconds

if __name__ == "__main__":
    main()
#ctrl+c to stop
