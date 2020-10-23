# packages we will need:
# numpy?
# matplotlib to show the chart each thyme
import datetime
import pandas
from pandas_datareader import data
import psycopg2
from psycopg2.extras import RealDictCursor
import configparser

config = configparser.ConfigParser()
config.read('main.conf')

conn = psycopg2.connect(
    user=config['Database']['user'],
    password=config['Database']['password'],
    host=config['Database']['host'],
    port=config['Database']['port'],
    database=config['Database']['database']
)

cur = conn.cursor(cursor_factory=RealDictCursor)
cur.execute("""
        SELECT * from mock_watchlist
        ORDER BY ticker ASC
        ;
    """)
res = cur.fetchall()
tickers = [x['ticker'] for x in res]
# currently have to tickers (BHP, CBA)
print("Tickers from db: {}".format(tickers))

# for now, just query one stock maybe NAB?
# make dataframe (build custom function that will take ticker, and start and end, and return the DF)
for tick in tickers:
    # for now just get 30 days
    end = datetime.date.today()
    start = end - datetime.timedelta(days=30)
    df = data.DataReader('{}.AX'.format(tick),
                         start=start,
                         end=end,
                         data_source='yahoo')[['High', 'Low', 'Open', 'Adj Close']]
    df['Up Today'] = df['Adj Close'] > df['Open']
    df['% Change'] = df['Adj Close'].pct_change(periods=1) * 100
    # Add moving averages?
    # Add momentum indicator?
    # Compute here what kind of candlestick it is (maybe only last ten?)
    print(df)
# build function that will take a candlestick and define it (ie, doji, etc, use the Bedford book for defintions)
