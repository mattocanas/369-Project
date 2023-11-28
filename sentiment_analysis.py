import pandas as pd
from transformers import pipeline


def nytSentiment():
    # Load the CSV file into a pandas DataFrame
    nyt_df = pd.read_csv("nyt_articles_2010-2019.csv")

    # Initialize the Hugging Face sentiment analysis pipeline
    sentiment_analysis = pipeline("sentiment-analysis")

    # analyze sentiment and return the result with score
    def analyze_sentiment(text):
        # check if text is empty
        if pd.isna(text) or text.strip() == "":
            return None, None
        if len(text) > 512:
            text = text[:512]
        result = sentiment_analysis(text)[0]
        return result["label"], result["score"]

    # Apply the function while skipping empty titles or snippets
    nyt_df["title_sentiment"], nyt_df["title_score"] = zip(
        *nyt_df["title"].apply(
            lambda x: analyze_sentiment(x)
            if pd.notnull(x) and x.strip() != ""
            else (None, None)
        )
    )
    nyt_df["snippet_sentiment"], nyt_df["snippet_score"] = zip(
        *nyt_df["snippet"].apply(
            lambda x: analyze_sentiment(x)
            if pd.notnull(x) and x.strip() != ""
            else (None, None)
        )
    )

    # Save the updated DataFrame to a new CSV file
    nyt_df.to_csv("nyt_sentiment.csv", index=False)


def guardianSentiment():
    guardian_df = pd.read_csv("guardian_full_articles.csv")

    # Initialize the Hugging Face sentiment analysis pipeline
    sentiment_analysis = pipeline("sentiment-analysis")

    # Function to analyze sentiment and return the result with score
    def analyze_sentiment(text):
        # Check if text is empty
        if pd.isna(text) or text.strip() == "":
            return None, None
        if len(text) > 512:  # Truncate if more than 512 characters
            text = text[:512]
        result = sentiment_analysis(text)[0]
        return result["label"], result["score"]

    # Apply the function while skipping empty titles or lead paragraphs
    guardian_df["title_sentiment"], guardian_df["title_score"] = zip(
        *guardian_df["Title"].apply(
            lambda x: analyze_sentiment(x)
            if pd.notnull(x) and x.strip() != ""
            else (None, None)
        )
    )
    guardian_df["snippet_sentiment"], guardian_df["snippet_score"] = zip(
        *guardian_df["article"].apply(
            lambda x: analyze_sentiment(x)
            if pd.notnull(x) and x.strip() != ""
            else (None, None)
        )
    )

    # Save the updated DataFrame to a new CSV file
    guardian_df.to_csv("guardian_sentiment.csv", index=False)


def main():
    nytSentiment()
    guardianSentiment()


if __name__ == "__main__":
    main()
