# This file contains code that uses the Guardian API to get article data, and then use webscraping to get the full article.
# This file runs each article and article title through a sentiment analysis pipeline


# Get article title, date, and URL
# Get data from 01/01/2012 - 01/01/2023

import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup


def search_guardian_articles(api_key, week_start_date, week_end_date):
    base_url = "http://content.guardianapis.com/search"
    params = {
        "section": "business",
        "from-date": week_start_date,
        "to-date": week_end_date,
        "api-key": api_key,
        "page-size": 3,  # retrieve top 3 articles
        "order-by": "relevance",
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {
            "error": "Request failed with status code {}".format(response.status_code)
        }


def generate_weekly_dates(from_date, to_date):
    start = datetime.datetime.strptime(from_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(to_date, "%Y-%m-%d")
    date_generated = [
        start + datetime.timedelta(days=x) for x in range(0, (end - start).days, 7)
    ]
    return date_generated


# The following code uses webscraping to get the full article text from the link
def read_articles():
    # Load the CSV file
    df = pd.read_csv("guardian_articles_no_story.csv")

    def get_article_text(url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                paragraphs = soup.find_all("p")
                article_text = " ".join(paragraph.text for paragraph in paragraphs)
                return article_text
        except requests.RequestException as e:
            return None

    df["article"] = df["URL"].apply(get_article_text)

    df.to_csv("guardian_full_articles.csv", index=False)


def main():
    api_key = "cfd34dfb-d992-484e-96f0-4618510cdb05"
    from_date = "2010-01-01"  # start date
    to_date = "2023-01-01"  # end date

    weekly_dates = generate_weekly_dates(from_date, to_date)

    article_data = []
    for start_date in weekly_dates:
        end_date = start_date + datetime.timedelta(days=3)
        end_date_str = end_date.strftime("%Y-%m-%d")
        start_date_str = start_date.strftime("%Y-%m-%d")

        articles = search_guardian_articles(api_key, start_date_str, end_date_str)
        if "error" not in articles:
            for article in articles["response"]["results"]:
                article_data.append(
                    {
                        "Title": article["webTitle"],
                        "Date": article["webPublicationDate"],
                        "URL": article["webUrl"],
                    }
                )

    df = pd.DataFrame(article_data)
    # display(df)
    df.to_csv("guardian_articles_no_story.csv")
    read_articles()


if __name__ == "__main__":
    main()
