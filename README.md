# 369-Project


# Documentation

## Package Requirements
* requests
* json
* pandas
* datetime
* time
* beautifulsoup4
* transformers


## Collecting Data
To begin using our code, the first thing you need to do is gather the data necessary for the data analysis. We utilize the API from _The New York Times_ and _The Guardian_. My API key is included in the repository, but keep in mind that if two people try running it on the same day with my key, it may be rate limited.

### nyt.py
First, let us collect data from the NYT. 
_nyt.py_ is configured in this repository to gather Business section articles from 2010-2019, or until the daily call limit is maxed out. Our dataset goes from 2010-2023. Doing this required us manually changing the start/end date, and running the script on two separate date to get around rate limiting. Future implementations should obviously automate this.


To get the 2010-2019 data, simply run _nyt.py_ using ```python3 nyt.py```

The output of this, assuming you have not changed the script, will be a file named _nyt_articles_2010-2019.csv_. This will soon be run through the sentiment analysis pipeline.

**NOTE:** This script, depending on the number of years being pulled, takes 2-4 hours to run. This is becuase we have to pause for 12 seconds after each API call to avoid rate limitations.

### guardian.py
Next, we will collect data from the guardian. Rate limiting is not an issue here, so simply set your start/end dates. In the case of the script in this repository, we will gather stories in the business section from 2010-2023.

_guardian.py_ pulls article titles, publication dates, and URLs from The Guardian API, and saves it as a CSV. It then runs that CSV through a function that uses Beautifulsoup to go to each article URL and scrape the webpage for the full story. It adds the full story to a pandas dataframe, and saves a new CSV file.


To run this, use ```python3 guardian.py```. A file named _guardian_full_articles.csv_ will be saved to the directory and uses to analyze news sentiments.

### sentiment_analysis.py
This script will run the two previously saved CSV files through the Hugging Face transformers sentiment-analysis pipeline to classify article titles and artricle content as **POSITIVE** or **NEGATIVE**.

This repository contains the correct CSV files such that all you need to do is run this file, and not have to edit any filename or run any previously discussed scripts.

![image](https://github.com/mattocanas/369-Project/assets/49545348/ca78e0fe-ffcd-40c0-848a-ef89d99b339d)

In the function above, ensure the file name corresponds to the CSV file you wish to run through the pipeline for the NYT data.

![image](https://github.com/mattocanas/369-Project/assets/49545348/8bb11fb2-81f1-4e4f-91e2-8905946837ef)

In the function above, ensure the file name corresponds to the CSV file you wish to run through the pipeline for The Guardian data.

After confirming you are running the correct CSV files through the pipeline, simply run ```python3 sentiment_analysis.py```. This will save two new CSV files to the directory: _nyt_sentiment.csv_ and _guardian_sentiment.csv_.

These are the two CSV files that will be used for downstream analysis.





