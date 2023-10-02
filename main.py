#import fire
from src.lib import read_data, pivot_by_price_type
from database import db_handler
import polars as pl
from src.download_currencies import create_tickers
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker


def insert_ccy_to_db(ccy):
    df = read_data("src/currency_prices_long.csv")
    ticker = create_tickers([ccy])
    ccy_df = df.filter(pl.col("Instrument") == ticker[0])
    ccy_df = pivot_by_price_type(ccy_df)

    conn = db_handler.create_connection("database/currencies.db")
    cursor = db_handler.create_cursor(conn)
    db_handler.create_ohlc_table("usdmxn", cursor, conn)
    db_handler.insert_ohlc(ccy, ccy_df, cursor, conn)
    conn.close()
    pass


def plot_ccy(table_name):
    conn = db_handler.create_connection("database/currencies.db")
    cursor = db_handler.create_cursor(conn)
    df = db_handler.db_to_df(table_name, cursor)
    conn.close()
    fig, ax = plt.subplots()
    ax.plot(df["Datetime"], df["Close"].pct_change().cumsum())
    plt.legend(table_name.upper())
    ax.set_ylabel("% change")
    ax.set_xlabel("Date")
    plt.xticks(rotation=45)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d%b"))
    plt.locator_params(axis="x", nbins=5)
    ax.xaxis.set_major_locator(plt.MaxNLocator(20))
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
    fig.suptitle("Currency returns")
    pass
