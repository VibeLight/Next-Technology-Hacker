import requests
from bs4 import BeautifulSoup

def scrape_web(config):
    try:
        response = requests.get(config["url"])
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        result = {}
        for key, selector in config["selectors"].items():
            element = soup.select_one(selector)
            result[key] = element.text.strip() if element else None
        return result
    except Exception as e:
        return {"error": str(e)}
