# 369-Project


# Documentation

## Collecting Data
To begin using our code, the first thing you need to do is gather the data necessary for the data analysis. We utilize the API from _The New York Times_ and _The Guardian_. My API key is included in the repository, but keep in mind that if two people try running it on the same day with my key, it may be rate limited.

### nyt.py
First, let us collect data from the NYT. 
_nyt.py_ is configured in this repository to gather Business section articles from 2010-2019, or until the daily call limit is maxed out. Our dataset goes from 2010-2023. Doing this required us manually changing the start/end date, and running the script on two separate date to get around rate limiting. Future implementations should obviously automate this.
The package requirements for this script are:
* requests
* json
* pandas
* datetime
* time

To get the 2010-2019 data, simply run _nyt.py_ using ```python3 nyt.py```

The output of this, assuming you have not changed the script, will be a file named _nyt_articles_2010-2019.csv_. This will soon be run through the sentiment analysis pipeline.

### guardian.py
Next, we will collect data from the guardian. Rate limiting is not an issue here, so simply set your start/end dates. In the case of the script in this repository, we will gather stories in the business section from 2010-2023.

