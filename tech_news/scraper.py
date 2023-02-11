import requests
import time
from parsel import Selector


def fetch(url):
    time.sleep(1)

    HEADER = {"user-agent": "Fake user-agent"}

    try:
        response = requests.get(url, headers=HEADER, timeout=5)
        if response.status_code == 200:
            return response.text
    except (requests.ReadTimeout, requests.HTTPError):
        return None


def scrape_updates(html_content):
    selector = Selector(html_content)
    return selector.css("h2.entry-title a::attr(href)").getall()


# Requisito 3
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 4
def scrape_news(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
