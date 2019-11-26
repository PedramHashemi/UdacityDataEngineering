import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """ this function takes creates the staging tables
    cur -- the cursor
    conn -- the connection
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """ this function executes the insert statements one by one from the insert_table_queries list
    cur -- the cursor
    conn -- the connection
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """ The main function creates a cursor and connectio. Then it creates and fills the stagin tables."""
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()