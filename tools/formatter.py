import json
from datetime import datetime

# Brand Colors
COLOR_BG = "#151515"
COLOR_PRIMARY = "#DEEBC8"
COLOR_ACCENT = "#6C757D"
COLOR_TEXT_BODY = "#E0E0E0"

def to_slack_blocks(articles):
    """
    Generates a Slack Block Kit JSON object for a list of articles.
    """
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"🚀 Scraperrr Intelligence Feed - {datetime.now().strftime('%Y-%m-%d')}",
                "emoji": True
            }
        },
        {"type": "divider"}
    ]
    
    for article in articles[:10]: # Limit to 10 for Slack to avoid hitting block limits
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{article['title']}*\n{article['source']} • <{article['url']}|Read Article>"
            }
        })
        blocks.append({"type": "divider"})
        
    if len(articles) > 10:
        blocks.append({
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"And {len(articles) - 10} more articles..."
                }
            ]
        })
        
    return {"blocks": blocks}

def to_notion_properties(article):
    """
    Generates a Notion API properties dictionary for a single article.
    Assumes a Database with 'Title' (title), 'URL' (url), 'Source' (select), 'Date' (date).
    """
    return {
        "Title": {
            "title": [
                {
                    "text": {
                        "content": article['title']
                    }
                }
            ]
        },
        "URL": {
            "url": article['url']
        },
        "Source": {
            "select": {
                "name": article['source']
            }
        },
        "Date": {
            "date": {
                "start": article['scraped_at'] # Or published_date if available
            }
        }
    }

def to_email_html(articles):
    """
    Generates a responsive HTML email body.
    """
    rows = ""
    for article in articles:
        rows += f"""
        <div style="background-color: rgba(255, 255, 255, 0.05); border: 1px solid #333; border-radius: 8px; padding: 16px; margin-bottom: 16px;">
            <div style="color: {COLOR_ACCENT}; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">{article['source']}</div>
            <h3 style="margin: 0 0 8px 0; font-family: 'Outfit', sans-serif; font-size: 18px; color: #ffffff;">
                <a href="{article['url']}" style="color: #ffffff; text-decoration: none;">{article['title']}</a>
            </h3>
            <a href="{article['url']}" style="display: inline-block; color: {COLOR_PRIMARY}; text-decoration: none; font-size: 14px; font-weight: bold;">Read Article &rarr;</a>
        </div>
        """
        
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Outfit:wght@700&display=swap');
        </style>
    </head>
    <body style="margin: 0; padding: 0; background-color: {COLOR_BG}; font-family: 'Inter', sans-serif; color: {COLOR_TEXT_BODY};">
        <div style="max-width: 600px; margin: 0 auto; padding: 40px 20px;">
            <div style="text-align: center; margin-bottom: 40px;">
                <h1 style="font-family: 'Outfit', sans-serif; font-size: 32px; margin: 0; color: {COLOR_PRIMARY};">SCRAPER<span style="color: {COLOR_ACCENT};">RR</span></h1>
                <p style="color: {COLOR_ACCENT}; font-size: 14px; text-transform: uppercase; letter-spacing: 2px; margin-top: 8px;">Intelligence Feed</p>
            </div>
            
            {rows}
            
            <div style="text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #333; color: {COLOR_ACCENT}; font-size: 12px;">
                &copy; {datetime.now().year} Scraperrr. All rights reserved.
            </div>
        </div>
    </body>
    </html>
    """
    return html

def to_html_report(articles):
    """
    Generates a standalone, professional HTML report file.
    Similar to email but full width and more dashboard-like features.
    """
    card_rows = ""
    for article in articles:
        date_str = datetime.fromisoformat(article['scraped_at']).strftime("%b %d") if 'scraped_at' in article else "N/A"
        
        card_rows += f"""
        <div class="card">
            <span class="source-tag">{article['source']}</span>
            <h3 class="card-title">{article['title']}</h3>
            <div class="card-footer">
                <span class="date">{date_str}</span>
                <a href="{article['url']}" target="_blank" class="read-more">Read &rarr;</a>
            </div>
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Scraperrr Intelligence Report</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@500;700&display=swap" rel="stylesheet">
        <style>
            :root {{
                --color-bg: {COLOR_BG};
                --color-primary: {COLOR_PRIMARY};
                --color-accent: {COLOR_ACCENT};
                --color-text: {COLOR_TEXT_BODY};
                --font-heading: 'Outfit', sans-serif;
                --font-body: 'Inter', sans-serif;
            }}
            
            body {{
                background-color: var(--color-bg);
                color: var(--color-text);
                font-family: var(--font-body);
                margin: 0;
                padding: 0;
                -webkit-font-smoothing: antialiased;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                padding: 4rem 2rem;
            }}
            
            .header {{
                text-align: center;
                margin-bottom: 4rem;
                padding-bottom: 2rem;
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }}
            
            .logo {{
                font-family: var(--font-heading);
                font-size: 4rem;
                font-weight: 700;
                color: var(--color-primary);
                margin: 0;
                line-height: 1;
            }}
            
            .logo span {{
                color: var(--color-accent);
            }}
            
            .subtitle {{
                color: var(--color-accent);
                font-size: 1.2rem;
                text-transform: uppercase;
                letter-spacing: 3px;
                margin-top: 1rem;
            }}
            
            .grid {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
                gap: 2rem;
            }}
            
            .card {{
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 12px;
                padding: 1.5rem;
                display: flex;
                flex-direction: column;
                transition: transform 0.2s ease, border-color 0.2s ease;
            }}
            
            .card:hover {{
                transform: translateY(-4px);
                border-color: var(--color-primary);
            }}
            
            .source-tag {{
                font-size: 0.75rem;
                color: var(--color-accent);
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 1rem;
            }}
            
            .card-title {{
                font-family: var(--font-heading);
                font-size: 1.5rem;
                color: #fff;
                margin: 0 0 1.5rem 0;
                line-height: 1.3;
            }}
            
            .card-footer {{
                margin-top: auto;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-top: 1px solid rgba(255,255,255,0.05);
                padding-top: 1rem;
            }}
            
            .date {{
                color: var(--color-accent);
                font-size: 0.875rem;
            }}
            
            .read-more {{
                color: var(--color-primary);
                text-decoration: none;
                font-weight: 600;
                transition: opacity 0.2s;
            }}
            
            .read-more:hover {{
                opacity: 0.8;
            }}
            
            @media (max-width: 768px) {{
                .container {{ padding: 2rem 1rem; }}
                .logo {{ font-size: 3rem; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <header class="header">
                <h1 class="logo">SCRAPER<span>RR</span></h1>
                <p class="subtitle">Weekly Intelligence Report</p>
                <p style="color: var(--color-accent); margin-top: 0.5rem;">Total Items: {len(articles)}</p>
            </header>
            
            <div class="grid">
                {card_rows}
            </div>
            
            <footer style="text-align: center; margin-top: 4rem; color: var(--color-accent); font-size: 0.875rem;">
                Generated by Scraperrr on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </footer>
        </div>
    </body>
    </html>
    """
    return html
