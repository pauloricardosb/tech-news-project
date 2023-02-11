import requests
import time
from parsel import Selector
from tech_news.database import create_news


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


def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    return selector.css("a.next.page-numbers::attr(href)").get()


def scrape_news(html_content):
    selector = Selector(html_content)
    raw_url = selector.css(".pk-share-buttons-facebook a::attr(href)").get()
    url_index = raw_url.index("=") + 1
    url = raw_url[url_index:]
    title = selector.css(".entry-title::text").get().strip()
    timestamp = selector.css(".meta-date::text").get()
    writer = selector.css(".author a::text").get()
    reading_time = selector.css(".meta-reading-time::text").re_first(r"\d+")
    summary = (
        selector.xpath('string(//div[@class="entry-content"]/p)')
        .get()
        .strip()
    )
    category = selector.css(".category-style .label::text").get()

    news = {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "reading_time": int(reading_time),
        "summary": summary,
        "category": category,
    }
    return news


def get_tech_news(amount):
    link_next_page = "https://blog.betrybe.com"

    links_list = []
    news = []

    while len(links_list) < amount:
        page_html = fetch(link_next_page)
        links_list.extend(scrape_updates(page_html))
        link_next_page = scrape_next_page_link(page_html)

    for link in links_list[:amount]:
        news.append(scrape_news(fetch(link)))

    create_news(news)
    return news
