import requests
from bs4 import BeautifulSoup

def scrape_headlines(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    headlines = soup.find_all("span", class_="titleline")
    return [h.text for h in headlines]

def save_headlines(headlines):
    try:
        with open("headlines.txt", "r") as f:
            existing = f.read().splitlines()
    except FileNotFoundError:
        existing = []
    
    with open("headlines.txt", "a") as f:
        for headline in headlines:
            if headline not in existing:
                f.write(headline + "\n")



def main():  
  headlines=scrape_headlines("https://news.ycombinator.com")
  print(headlines)
  save_headlines(headlines)

main()