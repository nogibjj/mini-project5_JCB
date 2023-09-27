import sqlite3

connection = sqlite3.connect("currencies.db")


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
    ccy_df_pivot["Datetime"].dt.strftime("%Y-%m-%d %H:%M:%S")
    for i in range(len(ccy_df_pivot)):
        cursor.execute(
            insert_query, ccy_df_pivot[i, ["Datetime", "Open", "High", "Low", "Close"]]
        )
        pass
    connection.commit()
    pass


def print_select_all(table_name, cursor):
    select_query = "SELECT * FROM {}".format(table_name)
    for i in cursor.execute(select_query):
        print(i)
        pass
