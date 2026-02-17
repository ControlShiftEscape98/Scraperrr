import json
import os
from datetime import datetime
from playwright.sync_api import sync_playwright
from supabase import create_client, Client

DATA_FILE = "data/articles.json"

# Supabase Credentials (Hardcoded for prototype simplicity)
SUPABASE_URL = "https://obubwbgwpsheugbhsbgl.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9idWJ3Ymd3cHNoZXVnYmhzYmdsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEyODk2MjUsImV4cCI6MjA4Njg2NTYyNX0.V-0_ypIetZpXUlADPqIk6TSP0MvZjeRUiDNNW6j3UOQ"

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"Failed to initialize Supabase client: {e}")
    supabase = None

def load_existing_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_data(articles):
    # Save local JSON
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(articles, f, indent=2)
    print(f"Saved {len(articles)} articles to {DATA_FILE}")
    
    # Save to Supabase
    if supabase and articles:
        try:
            # We must use upsert to avoid duplicates if URL is unique constraint
            response = supabase.table("articles").upsert(articles, on_conflict="url").execute()
            # Note: supabase-py v2 returns an object with 'data'
            print(f"Upserted {len(response.data) if response.data else 0} articles to Supabase.")
        except Exception as e:
            print(f"Error saving to Supabase: {e}")

def scrape_bensbites(page):
    print("Scraping Ben's Bites...")
    url = "https://www.bensbites.com/archive"
    page.goto(url, timeout=60000)
    page.wait_for_selector('div[role="article"]', timeout=30000)
    
    articles = []
    cards = page.query_selector_all('div[role="article"]')
    
    for card in cards:
        try:
            title_el = card.query_selector("a[class*='font-pub-headings']")
            date_el = card.query_selector("time")
            
            if not title_el:
                continue

            title = title_el.inner_text().strip()
            link = title_el.get_attribute("href")
            if link and not link.startswith("http"):
                link = "https://www.bensbites.com" + link
                
            date_str = date_el.inner_text().strip() if date_el else datetime.now().isoformat()
            
            articles.append({
                "source": "BensBites",
                "title": title,
                "url": link,
                "date": date_str,
                "scraped_at": datetime.now().isoformat()
            })
        except Exception as e:
            print(f"Error parsing card: {e}")
            continue
            
    print(f"Found {len(articles)} articles from Ben's Bites")
    return articles

def scrape_therundown(page):
    print("Scraping The Rundown...")
    url = "https://www.therundown.ai/archive"
    page.goto(url, timeout=60000)
    
    page.wait_for_selector('a.embla__slide__number, div.group', timeout=30000)
    
    articles = []
    cards = page.query_selector_all('a.embla__slide__number')
    
    for card in cards:
        try:
            link = card.get_attribute("href")
            if link and not link.startswith("http"):
                link = "https://www.therundown.ai" + link
            
            title_el = card.query_selector("h3")
            title = title_el.inner_text().strip() if title_el else "No Title"
            
            date_str = None 
            
            articles.append({
                "source": "TheRundown",
                "title": title,
                "url": link,
                "date": date_str,
                "scraped_at": datetime.now().isoformat()
            })
        except Exception as e:
            print(f"Error parsing card: {e}")
            continue

    print(f"Found {len(articles)} articles from The Rundown")
    return articles

def main():
    existing_articles = load_existing_data()
    existing_urls = {a["url"] for a in existing_articles}
    
    new_articles = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        page = context.new_page()
        
        try:
            bb_articles = scrape_bensbites(page)
            for a in bb_articles:
                # Add check if article already exists in json to avoid dups in json list
                # Supabase handles upsert via URL unique key
                new_articles.append(a)
                    
            tr_articles = scrape_therundown(page)
            for a in tr_articles:
                new_articles.append(a)
                    
        except Exception as e:
            print(f"Global Scraper Error: {e}")
        finally:
            browser.close()
            
    if new_articles:
        # Save ALL scraped articles to Supabase (upsert handles dups)
        # But only append NEW ones to local JSON to avoid massive file growth if we wanted history
        # For this logic, let's just save the batch we found to Supabase and update local JSON with unique ones
        print(f"Found {len(new_articles)} articles in this run.")
        save_data(new_articles)
    else:
        print("No articles found.")

if __name__ == "__main__":
    main()
