from tech_news.database import search_news
import datetime


def search_by_title(title):
    new = search_news({"title": {"$regex": title, "$options": "i"}})
    news_result = [(news["title"], news["url"]) for news in new]

    return news_result


def search_by_date(date):
    try:
        formatted_date = datetime.date.fromisoformat(date).strftime("%d/%m/%Y")
        new = search_news({"timestamp": formatted_date})
        news = [(news["title"], news["url"]) for news in new]
    except ValueError:
        raise ValueError('Data inválida')

    return news


def search_by_category(category):
    new = search_news({"category": {"$regex": category, "$options": "i"}})
    news = [(news["title"], news["url"]) for news in new]

    return news
