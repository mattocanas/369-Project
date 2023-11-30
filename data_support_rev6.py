import pandas as pd
import yfinance as yf

# process data, change column titles, add source column, change format so that date is in datetime format
def process_data(csv1, csv2):
    nyt_df = pd.read_csv(csv1)
    guard_df = pd.read_csv(csv2)

    cols = ['index', 'title', 'date', 'url', 'article', 'title_sentiment',
       'title_prob', 'article_sentiment', 'article_prob']
    
    nyt_df.columns = cols
    guard_df.columns = cols
    guard_df = guard_df.assign(source = 'Guardian')
    nyt_df = nyt_df.assign(source = 'New York Times')

    merge = guard_df.merge(nyt_df, how= 'outer')

    data = (
        merge.assign(datetime=lambda data: pd.to_datetime(data['date'].astype(str).str[:10], format="%Y-%m-%d"))
        .sort_values(by = 'datetime')
    )

    merge = merge.assign(Month=pd.to_datetime(merge['date']).dt.month)
    merge = merge.assign(Year=pd.to_datetime(merge['date']).dt.year)
    merge = merge.assign(YearMonth=lambda x: x['Year'].astype(str) + '-' + x['Month'].astype(str))
    merge['YearMonth'] = pd.to_datetime(merge['YearMonth'], format='%Y-%m')

    merge.to_csv('datatocheck.csv')

    return data

# get the percent different of stock values between the days! 
def stock_perc_change(df):
    df['PercentChange'] = None
    prev_close = 0

    for row in df.itertuples(index=True):
        if prev_close == 0:
            df.at[row.Index, 'PercentChange'] = 0
        else:
            df.at[row.Index, 'PercentChange'] = (prev_close - row.MeanClose) / prev_close * 100

        prev_close = row.MeanClose

    return df

def get_stock_percent_change(df, interval, stock):
    # get the desired dates 
    min_date = df["datetime"].min().date()
    max_date = df["datetime"].max().date()
    
    # Get stock data dependent on the ticker selected by the user
    obj = yf.Ticker(stock)
    all_stock_data = obj.history(start=min_date, end=max_date, interval='1D', actions = False, auto_adjust=True)
    all_stock_data.reset_index(inplace=True)
    all_stock_data.columns = ['date', 'Open', 'High', 'Low', 'Close', 'Volume']
    selected_columns = ['date', 'Close']
    some_stock_data = all_stock_data[selected_columns].copy()

    some_stock_data = some_stock_data.assign(Month=pd.to_datetime(some_stock_data['date']).dt.month)
    some_stock_data = some_stock_data.assign(Year=pd.to_datetime(some_stock_data['date']).dt.year)
    some_stock_data = some_stock_data.assign(YearMonth=lambda x: x['Year'].astype(str) + '-' + x['Month'].astype(str))
    some_stock_data['YearMonth'] = pd.to_datetime(some_stock_data['YearMonth'], format='%Y-%m')

    stock_df = some_stock_data.groupby(interval)["Close"].mean().reset_index(name='MeanClose')
    percent_df = stock_perc_change(stock_df)

    return percent_df

# calculate summary statistics
def sentiment_summary(merge, interval, stock):
    # Create monthly and annual dates to process dataframe
    merge = merge.assign(Month=pd.to_datetime(merge['date']).dt.month)
    merge = merge.assign(Year=pd.to_datetime(merge['date']).dt.year)
    merge = merge.assign(YearMonth=lambda x: x['Year'].astype(str) + '-' + x['Month'].astype(str))
    merge['YearMonth'] = pd.to_datetime(merge['YearMonth'], format='%Y-%m')
    stock_df = get_stock_percent_change(merge, interval, stock)

    # Group by the new interval column and count of articles types or average scores given desired user input
    pos_title = merge.groupby(interval)["title_sentiment"].apply(lambda x: (x == 'POSITIVE').sum()).reset_index(name='PositiveTitleCount')
    neg_title = merge.groupby(interval)["title_sentiment"].apply(lambda x: (x == 'NEGATIVE').sum()).reset_index(name='NegativeTitleCount')
    pos_article = merge.groupby(interval)["article_sentiment"].apply(lambda x: (x == 'POSITIVE').sum()).reset_index(name='PositiveArticleCount')
    neg_article = merge.groupby(interval)["article_sentiment"].apply(lambda x: (x == 'NEGATIVE').sum()).reset_index(name='NegativeArticleCount')

    # Merge counts for titles and articles
    title_count = pos_title.merge(neg_title, on=interval, how='outer')
    article_count = pos_article.merge(neg_article, on=interval, how='outer')
    df = title_count.merge(article_count, on=interval, how='outer')
    
    # simple calculations user may be interested in
    df = df.assign(percent_neg_titles = lambda x: x['NegativeTitleCount']/ (x['NegativeTitleCount'] + x['PositiveTitleCount'])*100)
    df = df.assign(percent_neg_articles = lambda x: x['NegativeArticleCount']/ (x['NegativeArticleCount'] + x['PositiveArticleCount'])*100)
    df = df.assign(percent_postitle_negarticle=lambda x: (x['PositiveTitleCount'] - x['PositiveArticleCount'])/ (x['PositiveArticleCount'] + x['NegativeArticleCount'])*100)
    df = df.assign(percent_dif_sentiment = lambda x: abs(x['percent_postitle_negarticle']))
    df = df.assign(time = df[interval])

    combined_df = df.merge(stock_df, on=interval, how='outer')
    return combined_df

# options set is referenced for drop down, etc.
options = [
{"label": '% Negative Titles', "value": 'percent_neg_titles'},
{"label": '% Negative Articles', "value": 'percent_neg_articles'},
{"label": '% Negative Article with Positive Title', "value": 'percent_postitle_negarticle'},
{"label": '% Opposite Sentiment', "value": 'percent_dif_sentiment'},
]

stocks = [
    {"label": 'NASDAQ', "value": 'SPY'},
    {"label": 'S&P 500', "value": '^IXIC'},
    {"label": 'Dow Jones', "value": '^DJI'},
]

# pick desired colors
def get_color(key, source):
    color_key = [
    {"label": '% Negative Titles', "New York Times": "#3498db", "Guardian": "#1abc9c"},
    {"label": '% Negative Articles', "New York Times": "#e74c3c", "Guardian":"#9b59b6"},
    {"label": '% Negative Article with Positive Title', "New York Times": "#2ecc71", "Guardian": "#f39c12"},
    {"label": '% Opposite Sentiment', "New York Times": "#f39c12", "Guardian": "#27ae60"},
    ]

    for entry in color_key:
        if entry["label"] == key:
            return entry[source]
    return None  # Return None if the label is not found

# get key/value
def get_key_by_value(value, options):
    for option in options:
        if option["value"] == value:
            return option["label"]
    return None  # Return None if the value is not found

def get_stock_by_value(value, stocks):
    for stock in stocks:
        if stock["value"] == value:
            return stock["label"]
    return None  # Return None if the value is not found

# generate data for the summary statistics plot
def generate_data(list, source, interval, data, options, stock):
    summary_df = sentiment_summary(data, interval, stock)
    plot_data = []
    
    # Get color and label! 
    key = get_key_by_value(list[0], options)

    # this will be used in the option value to display all of the stats too the user
    plot_data.append({"x": summary_df["time"],
                "y": summary_df[list[0]],
                "type": "lines",
                "hovertemplate": "%{y:.2f}%<extra></extra>",
                "name": str(source[0]) + " " + str(key),
                "line": {"color": get_color(key, source[0]),
                        "width": 2.5}}) 
    return plot_data

# plot raw data for reference to user
def raw_plot(source, data):
    plot_data = []
    if source == 'New York Times':
        c1 = "#3498db"
        c2 = "#f39c12"
    else:
        c1 = "#2ecc71"
        c2 = "#e74c3c"
    
    # iterate 4 times for...
    # two times for color based on title/ article
    # two times for shape based on negative/ positive 
    types = {'NEGATIVE': 'diamond', 'POSITIVE': 'circle'}
    contents = {'title_sentiment': c1, 'article_sentiment': c2}

    for sentiment_type in types:
        for key in contents:
            # query data that is based on sentiment and article/ title
            inter_data = data.query(f'{key} == "{sentiment_type}"')

            # Plot title/ article probability
            plot_data.append(
                {"x": inter_data["datetime"],
                "y": inter_data[f'{key.replace("_sentiment", "")}_prob'],
                "type": "lines",
                "hovertemplate": "%{y:.2f}<extra></extra>",
                "name": f'{source} {sentiment_type} {key}',
                "mode": 'markers',
                'marker': {'size': 5,
                        'color': contents[key],
                        'symbol': types[sentiment_type]},
                })

    return plot_data

def generate_stock_data(source, interval, data, stock):
    summary_df = sentiment_summary(data, interval, stock)
    stock_data = []
    
    if source == 'New York Times':
        c1 = "#3498db"
        c2 = "#f39c12"
    else:
        c1 = "#2ecc71"
        c2 = "#e74c3c"
    
    # iterate 4 times for...
    # two times for color based on title/ article
    # two times for shape based on negative/ positive 
    percent_neg = {'% Negative Titles': 'percent_neg_titles', '% Negative Articles': 'percent_neg_articles'}
    color = {'% Negative Titles': c1, '% Negative Articles': c2}

    for key in percent_neg: 
        # this will be used in the option value to display all of the stats too the user
        stock_data.append({"x": summary_df[percent_neg[key]],
                    "y": summary_df['PercentChange'],
                    "type": "lines",
                    "hovertemplate": "%{y:.2f}%<extra></extra>",
                    "name": str(source) + " " + str(key) + ' ' + get_stock_by_value(stock, stocks),
                    "mode": 'markers',
                    'marker': {'size': 5, "color": color[key]},
        })
    return stock_data

#data = process_data('nyt_sentiment.csv', 'guardian_sentiment.csv')
#sentiment_summary(data, 'YearMonth', 'SPY')
