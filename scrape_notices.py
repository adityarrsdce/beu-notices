import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

def scrape_beu_notices():
    url = "https://beu-bih.ac.in/notification"
    base_url = "https://beu-bih.ac.in/"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    notices = []

    for row in soup.select('table tr')[1:]:  # Skip table header
        cols = row.find_all("td")
        if len(cols) >= 2:
            date_text = cols[0].get_text(strip=True)
            title_tag = cols[1].find("a")
            if title_tag and ".pdf" in title_tag['href']:
                title = title_tag.get_text(strip=True)
                href = title_tag['href']
                full_url = href if href.startswith("http") else base_url + href.lstrip('/')

                notices.append({
                    "date": date_text,
                    "title": title,
                    "url": full_url
                })

    # Save to JSON
    with open("notices.json", "w", encoding='utf-8') as f:
        json.dump(notices, f, indent=2, ensure_ascii=False)

    print(f"✅ Scraped {len(notices)} notices with date and saved to notices.json")

if __name__ == "__main__":
    scrape_beu_notices()
