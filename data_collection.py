import pandas as pd
import yfinance as yf # pip install yfinance

# stocks, length, step size, and export file
listings = ['MMM', 'AXP', 'AMGN', 'AAPL', 'BA', 'CAT', 'CVX', 'CSCO', 'KO', 'DIS', 'DOW', 'GS', 'HD', 'HON', 'IBM', 'INTC', 'JNJ', 'JPM', 'MCD', 'MRK', 'MSFT', 'NKE', 'PG', 'CRM', 'TRV', 'UNH', 'VZ', 'V', 'WBA', 'WMT', 'DIA']
time = '20y'
timestep = '1d'
file = 'djia_data.csv'


def get_dividends(stock, col_name):
    # get historical dividend info for each stock
    div_series = yf.Ticker(stock).dividends
    dividend_df = div_series.to_frame(name=col_name)
    # remove time component from datetime index
    dividend_df.index = dividend_df.index.tz_convert(None).floor('D')
    return dividend_df

df = yf.download(tickers=listings, period=time, interval=timestep, auto_adjust=False)

# stack and unstack indexed columns
df = df.stack(level=0).unstack(level=1)

# set each column name to TICKER - VALUE
df.columns = df.columns.map(lambda x: f'{x[0]} - {x[1]}')

# create date column from index
df = df.reset_index()
df = df.rename(columns={'index': 'Date'})

for stock in listings:
    col_name = f'{stock} - Dividend'
    div_df = get_dividends(stock, col_name)
    df = pd.merge(df, div_df, left_on='Date', right_index=True, how='left')
    df[col_name] = df[col_name].fillna(0)

# export stock data to csv
df.to_csv(file, index=False)