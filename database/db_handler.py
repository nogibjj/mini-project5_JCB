import sqlite3
import polars as pl


def create_connection(db_file):
    """create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return None


def create_cursor(connection):
    try:
        cursor = connection.cursor()
        return cursor
    except sqlite3.Error as e:
        print(e)

    return None


def create_ohlc_table(table_name, cursor, connection):
    table = "CREATE TABLE {} (ccy TEXT, datetime TEXT, open FLOAT, high FLOAT, low FLOAT, close FLOAT)".format(
        table_name
    )
    cursor.execute(table)
    connection.commit()
    pass


def insert_ohlc(table_name, ccy_df_pivot, cursor, connection):
    insert_query = "INSERT INTO {} (datetime, open, high, low, close) VALUES(?, ?, ?, ?, ?)".format(
        table_name
    )
    ccy_df_pivot = ccy_df_pivot.with_columns(
        ccy_df_pivot["Datetime"].dt.strftime("%Y-%m-%d %H:%M:%S")
    )
    for row in ccy_df_pivot[["Datetime", "Open", "High", "Low", "Close"]].iter_rows():
        cursor.execute(insert_query, row)
        pass
    connection.commit()
    pass


def print_select_all(table_name, cursor):
    select_query = "SELECT * FROM {}".format(table_name)
    for i in cursor.execute(select_query):
        print(i)
        pass
    pass


def db_to_df(table_name, cursor):
    select_query = "SELECT * FROM {}".format(table_name)
    df = pl.DataFrame(cursor.execute(select_query))
    df = df.rename(
        {
            "column_1": "Datetime",
            "column_2": "Open",
            "column_3": "High",
            "column_4": "Low",
            "column_5": "Close",
        }
    )
    return df
