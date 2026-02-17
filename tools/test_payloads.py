import json
import os
import sys

# Add current directory to path so we can import tools modules
sys.path.append(os.getcwd())

from tools.formatter import to_slack_blocks, to_notion_properties, to_email_html, to_html_report

DATA_FILE = "data/articles.json"
PAYLOAD_DIR = "payloads"

def main():
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found. Run scraper first.")
        return

    with open(DATA_FILE, "r") as f:
        articles = json.load(f)

    if not articles:
        print("No articles found in data file.")
        return

    os.makedirs(PAYLOAD_DIR, exist_ok=True)

    # 1. Slack
    try:
        slack_payload = to_slack_blocks(articles)
        with open(f"{PAYLOAD_DIR}/slack_message.json", "w") as f:
            json.dump(slack_payload, f, indent=2)
        print(f"✅ Generated {PAYLOAD_DIR}/slack_message.json")
    except Exception as e:
        print(f"❌ Failed to generate Slack payload: {e}")

    # 2. Notion (Sample for first article)
    try:
        if articles:
            notion_payload = to_notion_properties(articles[0])
            with open(f"{PAYLOAD_DIR}/notion_sample.json", "w") as f:
                json.dump(notion_payload, f, indent=2)
            print(f"✅ Generated {PAYLOAD_DIR}/notion_sample.json")
    except Exception as e:
        print(f"❌ Failed to generate Notion payload: {e}")

    # 3. Email HTML
    try:
        email_html = to_email_html(articles[:5]) # Access top 5 for email preview
        with open(f"{PAYLOAD_DIR}/email_preview.html", "w") as f:
            f.write(email_html)
        print(f"✅ Generated {PAYLOAD_DIR}/email_preview.html")
    except Exception as e:
        print(f"❌ Failed to generate Email output: {e}")

    # 4. Professional Report HTML
    try:
        report_html = to_html_report(articles)
        with open(f"{PAYLOAD_DIR}/report.html", "w") as f:
            f.write(report_html)
        print(f"✅ Generated {PAYLOAD_DIR}/report.html")
    except Exception as e:
        print(f"❌ Failed to generate Professional Report: {e}")

if __name__ == "__main__":
    main()
