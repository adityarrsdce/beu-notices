import requests
from bs4 import BeautifulSoup
import json

def scrape_beu_notices():
    url = "https://beu-bih.ac.in/notification"
    base_url = "https://beu-bih.ac.in/"
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    notices = []
    
    # Find table rows
    rows = soup.select('table tr')[1:]  # Skip header

    for row in rows:
        columns = row.find_all("td")
        if len(columns) >= 3:
            date = columns[1].get_text(strip=True)
            title = columns[2].get_text(strip=True)
            link_tag = columns[3].find("a")
            url = base_url + link_tag['href'].lstrip('/') if link_tag else ""

            if title and url:
                notices.append({
                    "date": date,
                    "title": title,
                    "url": url
                })

    # Save to JSON
    with open("notices.json", "w", encoding='utf-8') as f:
        json.dump(notices, f, indent=2, ensure_ascii=False)

    print(f"✅ Scraped {len(notices)} notices from table")

if __name__ == "__main__":
    scrape_beu_notices()
