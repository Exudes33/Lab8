import psycopg2
from config import load_config

def test_connection():
    try:
        params = load_config()
        conn = psycopg2.connect(**params)
        crsr = conn.cursor()
        crsr.execute('SELECT version()')
        db_version = crsr.fetchone()
        print(db_version[0])
        crsr.close()
        conn.close()
    except Exception as error:
        print(error)

if __name__ == '__main__':
    test_connection()