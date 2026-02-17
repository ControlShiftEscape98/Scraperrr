# SOP: AI News Scraper

## Goal
Fetch the latest newsletter issues from Ben's Bites and The AI Rundown archives, extract article metadata, and save to a standardized JSON format.

## Tools
- `tools/scraper.py`: Main execution script using Python & Playwright.

## Input
- URLs: 
    - `https://www.bensbites.com/archive`
    - `https://www.therundown.ai/archive`

## Process
1. **Fetch**: Launch Playwright browser (headless).
2. **Navigate**: Go to target archive URL.
3. **Wait**: Ensure page content is loaded (network idle).
4. **Parse**:
    - Identify article container elements.
    - Extract `title`, `url`, `date`.
    - Normalize `date` to ISO8601.
    - Tag source (`BensBites` or `TheRundown`).
5. **Deduplicate**: Check against existing `data/articles.json` (by URL).
6. **Save**: Append new articles to `data/articles.json`.

## Edge Cases
- **Network Error**: Retry 3 times with exponential backoff.
- **Selector Change**: Log error and continue to next source.
- **Empty Page**: Verify if anti-bot triggered; log screenshot.

## Output
- `data/articles.json`: JSON Array of Article Objects.
