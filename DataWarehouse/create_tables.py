import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """ Drops the analytics tables
    cur -- cursor
    conn -- connection
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """ creates the analytics table in redshift
    cur -- cursor
    conn -- connection
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """ 
    This function deletes all the tables in redshift. then creates all the analytics tables.
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()