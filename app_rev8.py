import data_support_rev6 as ds

import pandas as pd
from dash import Dash, Input, Output, dcc, html

# Process data
data = ds.process_data('nyt_sentiment.csv', 'guardian_sentiment.csv')

# Import options to be used throughout this script from support file
filter_options=ds.options

# Create news source options with available sources
sources = data["source"].sort_values().unique()
sources = list(sources)  # Convert the array to a list

# Specify external style sheet and use font family 'Lato'
# Also note that there is additional style parameters in style.css in the assets filder
external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]

# Create instance of Dash class
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "New York Times and Guardian Sentiment Analysis"

# Define app layout in html format ie (header, selection tools, graphs)
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="", className="header-emoji"),
                html.H1(
                    children="Newspaper Sentiment and Market Behavior Analysis"
                    , className="header-title"
                ),
                html.P(
                    children=(
                        "Sentiment Analysis for Guardian and NYT Articles from 2010 - 2023"
                    ),
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                children=[
                    html.Div(children="Source", className="menu-title"),
                    dcc.Checklist(
                        id="source-filter",
                        options=sources,
                        value=['New York Times'],
                        className="dropdown",
                            ),
                        ],
                    ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range", className="menu-title"
                        ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data["datetime"].min().date(),
                            max_date_allowed=data["datetime"].max().date(),
                            start_date= data['datetime'].quantile(0.75).date(),
                            end_date=data["datetime"].max().date(),
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.Div(children="Interval", className="menu-title"),
                                dcc.Dropdown(
                                    id="interval-selection",
                                    options=[
                                        {'label': 'Month', 'value': 'YearMonth'},
                                        {'label': 'Year', 'value': 'Year'}
                                    ],
                                    value='YearMonth',
                                    clearable=False,
                                    className="dropdown",
                                ),
                            ]
                        ),
                    ], 
                ),  
            html.Div(
                children=[
                    html.Div(children="Trend", className="menu-title"),
                    dcc.Checklist(
                        id="trend-filter",
                        options=ds.options,
                        value=['percent_neg_titles'],
                        className="dropdown",
                            ),
                        ],
                    ),
            html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.Div(children="Stock Index", className="menu-title"),
                                dcc.Dropdown(
                                    id="stock-filter",
                                    options=ds.stocks,
                                    value='SPY',
                                    clearable=False,
                                    className="dropdown",
                                ),
                            ]
                        ),
                    ], 
                ),  
            ],
            className="wrapper",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="stats-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="sentiment-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="stock-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ] 
) 

# Update figures when parameters change
# Specify which ids and values are inputs/ outputs
@app.callback(
    [Output("sentiment-chart", "figure"),
     Output("stats-chart", "figure"),
     Output('stock-chart', "figure")],
    [Input("source-filter", "value"),
     Input("date-range", "start_date"),
     Input("date-range", "end_date"),
     Input("interval-selection", "value"),
     Input("trend-filter", "value"),
     Input("stock-filter", "value")]
)

# Update function
def update_charts(sources, start_date, end_date, interval, trends, stock):
    # Filter with start/ end date 
    time_range_data = data.query('date >= @start_date and date <= @end_date')
    plot_data = []
    # iterate through sources provided if multiple sources are selected 
    for source in sources:
        inter_data = time_range_data.query("source == @source")
        for trend in trends:
            temp_data = ds.generate_data([trend], [source], interval, inter_data, filter_options, stock)
            plot_data.extend(temp_data)

    stat_chart_figure = {
        "data": plot_data,
        "layout": {
            "title": {
                "text": "Newspaper Sentiment Summary",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True, "title": 'Time'},
            "yaxis": {"tickprefix": "", "fixedrange": True, "title": "Percentage"},
        },
    }

    # use similar logic to update the raw data chart given user selections
    raw_data = []
    for source in sources:
        inter_data = time_range_data.query("source == @source")
        another_temp_data = ds.raw_plot(source, inter_data)
        raw_data.extend(another_temp_data)

    sentiment_chart_figure = {
        "data": raw_data
        ,
        "layout": {
            "title": {
                "text": "Sentiment Probability Raw Data",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True, "title": 'Time'},
            "yaxis": {"tickprefix": "", "fixedrange": True, "title": 'Raw Score'},
            "colorway": ["#17B897"],
        },
    }

    stock_data = []
    for source in sources:
        inter_data = time_range_data.query("source == @source")
        temp_data = ds.generate_stock_data(source, interval, inter_data, stock)
        stock_data.extend(temp_data)
    
    # plot % negative titles, % negative articles v. % change in stock price
    stock_chart_figure = {
        "data": stock_data
        ,
        "layout": {
            "title": {
                "text": "Sentiment v. Index Stock % Change",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True, "title": '% Negative Sentiment'},
            "yaxis": {"tickprefix": "", "fixedrange": True, "title": 'Stock % Change'},
            "colorway": ["#17B897"],
        },
    }

    return sentiment_chart_figure, stat_chart_figure, stock_chart_figure

# run application!
if __name__ == "__main__":
    app.run_server(debug=True)