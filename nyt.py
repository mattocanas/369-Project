# This file contains code that uses the New York Times API to gather article data from the business section.
# Due to rate limiting, in order to get data from 2010-2023, you will either need swap API keys, or do half of it one day, and the other the next day.

# Get title, date, link, and lead paragraph which we will treat as the article

import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import time


def search_nyt_articles(
    api_key, section, begin_date, end_date, limit=3
):  # change the limit to the number of artilces
    # you want from each week
    base_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    fq = f'news_desk:("{section}")'
    params = {
        "fq": fq,
        "begin_date": begin_date,
        "end_date": end_date,
        "sort": "relevance",  # sort by newest, oldest, or relevance
        "api-key": api_key,
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raises an error if the HTTP request returned an failed status code
        articles = response.json().get("response", {}).get("docs", [])
        return articles[:limit]
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []


def get_weekly_articles(api_key, section, start_year):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(
        start_year + 10, 1, 1
    )  # change form +10, to + the number of years after
    # start_year you want to get data from

    all_articles = []

    while start_date < end_date:
        week_end = start_date + timedelta(days=6)
        formatted_start = start_date.strftime("%Y%m%d")
        formatted_end = week_end.strftime("%Y%m%d")

        articles = search_nyt_articles(api_key, section, formatted_start, formatted_end)

        for article in articles:
            article_data = {
                "title": article.get("headline", {}).get("main", ""),
                "date": article.get("pub_date", ""),
                "url": article.get("web_url", ""),
                "snippet": article.get("snippet", ""),
            }
            all_articles.append(article_data)

        start_date += timedelta(days=7)
        time.sleep(12)  # NYT API requires 12 seconds betweeen calls

    return pd.DataFrame(all_articles)


def main():
    api_key = "YHfI1weuElAq3KfFoQVDA2bDQ7ggkdsS"
    section = "Business"
    start_year = 2010

    df = get_weekly_articles(api_key, section, start_year)
    # print(df)
    df.to_csv("nyt_articles_2010-2019.csv")


if __name__ == "__main__":
    main()
