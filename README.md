# Changes in News Sentiment Over the Last Decade and its Effect on Financial Markets


# Documentation

## Background
For this project, we were curious about leveraging natural language processing to analyze how news coverage has changed over the last decade. Specifically, we wanted to find out if news outlets have become more negative in their reporting and coverage, and if they have begun to use titles that misrepresent a story to gain interactions. We decided to take this a step further, and see if such changes in sentiment were correlated with real world effects, such as performance of the financial markets.

To achieve this, we utilize APIs from major news outlets to pull historical articles and run them through a transformer model pretrained to analyze and classify sentiment as **POSITVIE or NEGATIVE**.

------
## How to run our project
First install the requirements shown below. Then, please run the files in the order shown below. More information on each file and how to run it is in subsequent sections. Please not that running the _nyt.py_ and _guardian.py_ may take upwards of 2 hours to complete. However, the files they are supposed to output are already included in the repository. Thus, you can skip those if you wish!

1. nyt.py
2. guardian.py
3. sentiment_analysis.py
4. nyt_stats.py
5. app_rev8.py
------


## Package Requirements
* requests
* json
* pandas
* datetime
* time
* beautifulsoup4
* transformers
* seaborn
* statsmodels.api


## Collecting Data
To begin using our code, the first thing you need to do is gather the data necessary for the data analysis. We utilize the API from _The New York Times_ and _The Guardian_. My API key is included in the repository, but keep in mind that if two people try running it on the same day with my key, it may be rate limited.

### nyt.py
First, let us collect data from the NYT. 
_nyt.py_ is configured in this repository to gather Business section articles from 2010-2019, or until the daily call limit is maxed out. Our dataset goes from 2010-2023. Doing this required us manually changing the start/end date, and running the script on two separate date to get around rate limiting. Future implementations should obviously automate this.


To get the 2010-2019 data, simply run _nyt.py_ using ```python3 nyt.py```

The output of this, assuming you have not changed the script, will be a file named _nyt_articles_2010-2019.csv_. This will soon be run through the sentiment analysis pipeline.

**NOTE:** This script, depending on the number of years being pulled, takes 2-4 hours to run. This is becuase we have to pause for 12 seconds after each API call to avoid rate limitations.

-----
### guardian.py
Next, we will collect data from the guardian. Rate limiting is not an issue here, so simply set your start/end dates. In the case of the script in this repository, we will gather stories in the business section from 2010-2023.

_guardian.py_ pulls article titles, publication dates, and URLs from The Guardian API, and saves it as a CSV. It then runs that CSV through a function that uses Beautifulsoup to go to each article URL and scrape the webpage for the full story. It adds the full story to a pandas dataframe, and saves a new CSV file.


To run this, use ```python3 guardian.py```. A file named _guardian_full_articles.csv_ will be saved to the directory and uses to analyze news sentiments.

------
### sentiment_analysis.py
This script will run the two previously saved CSV files through the Hugging Face transformers sentiment-analysis pipeline to classify article titles and artricle content as **POSITIVE** or **NEGATIVE**.

This repository contains the correct CSV files such that all you need to do is run this file, and not have to edit any filename or run any previously discussed scripts.

![image](https://github.com/mattocanas/369-Project/assets/49545348/ca78e0fe-ffcd-40c0-848a-ef89d99b339d)

In the function above, ensure the file name corresponds to the CSV file you wish to run through the pipeline for the NYT data.

![image](https://github.com/mattocanas/369-Project/assets/49545348/8bb11fb2-81f1-4e4f-91e2-8905946837ef)

In the function above, ensure the file name corresponds to the CSV file you wish to run through the pipeline for The Guardian data.

After confirming you are running the correct CSV files through the pipeline, simply run ```python3 sentiment_analysis.py```. This will save two new CSV files to the directory: _nyt_sentiment.csv_ and _guardian_sentiment.csv_.

These are the two CSV files that will be used for downstream analysis.

------
## Basic Statistical Analysis
Make sure that _nyt_sentiment.csv_ is in the same directory as _nyt_stats.py_. Then run ```python3 nyt_stats.py```. This will output the Ordinary Least Square Regression report and the seabron plots.

## Jaxon's section

## Dashboard Overview
The purpose of the dashboard is to create an interactive way for users to manipulate the data. The dashboard displays three charts. 

1. Newspaper Sentiment Summary

2. Sentiment Probability Raw Data

3. Sentiment v. Index Stock % Change

![image](https://github.com/mattocanas/369-Project/assets/98493997/137ddd1d-e144-4cb0-9a9d-76d1ebe55dd7)

![image](https://github.com/mattocanas/369-Project/assets/98493997/d69bd3f8-62c0-4bb6-86a9-c90c6a81c7a5)

![image](https://github.com/mattocanas/369-Project/assets/98493997/cc6af2d1-b219-454a-b1b0-9302672a02c3)

The user is also able to filter these charts using four filters.

1. Source (ie. New York Times or Guardian)

2. Interval (Monthly or Annually)

3. Trend (% Negative Titles, % Negative Articles, % Negative Article with Positive Title, and % Opposite Sentiment) 

4. Stock Index (NASDAQ, S&P 500, and Dow Jones)

   ![image](https://github.com/mattocanas/369-Project/assets/98493997/040538c2-ba58-4c06-afcd-79e539db180e)

To access the dashboard from a web browser, you will run the main script: app_rev8.py. The assets folder contains style parameters for the application. There is a file with support functions and data that performs the analysis for variables selected by the user in the data_support_rev6 file. 

### app.py
The app.py script is the main script. Run this to generate the dashboard! The main packages required are pandas and dash. In this script, dash is used to customize the style of the application, create callbacks to make the application interactive, and use dash core components/ html components to define the application.

Dash uses three technologies: flask, react.js, and plotly.js.

There are four sections of the script.

1. Process data

2. Style application with CSS.

3. Define content of the application using the layout function.

4. Create callbacks to make the application interactive.

The layout is defined by app.layout(). 

Key script features:

1. Create dash instance.

app = Dash(__name__, external_stylesheets=external_stylesheets)

2. Define application layout. Dash HTML Components module provides python wrappers to create elements like paragraphs or headings!

html.P(children="", className="header-emoji")

***Note:***

className pulls style information from the style.css file provided in the assets folder.

![image](https://github.com/mattocanas/369-Project/assets/98493997/7390e939-5c47-4f38-a154-57fd3f271b23)


3. Create interactive components like dropdowns and checklists using dash core components.

dcc.Dropdown(
            id="interval-selection",
            options=[
                {'label': 'Month', 'value': 'YearMonth'},
                {'label': 'Year', 'value': 'Year'}
            ],

4. Update the dashboard using callback functions using the app.callback decorator.

- Define inputs and outputs using @app.callback()

- Update charts using inputs

- The process_data_rev8 script handles the data manipulation to update the plots! 
