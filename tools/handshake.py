import playwright
from playwright.sync_api import sync_playwright

def handshake():
    print("Initializing Handshake...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        targets = [
            "https://www.bensbites.com/archive",
            "https://www.therundown.ai/archive"
        ]
        
        for url in targets:
            try:
                print(f"Connecting to {url}...")
                page = context.new_page()
                response = page.goto(url, timeout=30000)
                if response and response.status < 400:
                    print(f"SUCCESS: {url} responded with {response.status}")
                else:
                    print(f"FAILURE: {url} responded with {response.status if response else 'No Response'}")
                page.close()
            except Exception as e:
                print(f"ERROR: Failed to connect to {url}: {e}")
        
        browser.close()
    print("Handshake Complete.")

if __name__ == "__main__":
    handshake()
