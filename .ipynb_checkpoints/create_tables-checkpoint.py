import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def create_database():
    """ 
    Create sparkify database
    
    Parameters: 
    None
  
    Returns: 
    cur: cursor to sparkify database
    conn: connection to sparkify database
    """
    
    # connect to default database
    conn = psycopg2.connect("host=127.0.0.1 dbname=studentdb user=student password=student")
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    
    # create sparkify database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS sparkifydb")
    cur.execute("CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to default database
    conn.close()    
    
    # connect to sparkify database
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()
    
    return cur, conn


def drop_tables(cur, conn):
    """ 
    Drop tables in sparkify database
    
    Parameters: 
    cur: cursor to sparify database
    conn: connection to sparify database
  
    Returns: 
    None
    """
        
    for query in drop_table_queries:
        print(query)
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """ 
    Create tables in sparkify database
    
    Parameters: 
    cur: cursor to sparify database
    conn: connection to sparify database
  
    Returns: 
    None
    """
        
    for query in create_table_queries:
        print(query)
        cur.execute(query)
        conn.commit()


def main():
    """ 
    Create sparkify database, drop and create tables
    
    Parameters: 
    None
  
    Returns: 
    None
    """
    
    # create Sparkify database; return cursor and connection
    cur, conn = create_database()
    
    # drop tables in Sparkify database
    drop_tables(cur, conn)
    
    # create tables in Sparkify database
    create_tables(cur, conn)

    # close all connections
    conn.close()


if __name__ == "__main__":
    main()
    