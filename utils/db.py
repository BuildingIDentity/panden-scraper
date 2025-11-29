import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise Exception("DATABASE_URL is not set in environment variables.")
    return psycopg2.connect(db_url, sslmode='require')

def init_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS panden (
            id SERIAL PRIMARY KEY,
            bron TEXT,
            extern_id TEXT,
            type TEXT,
            particulier BOOLEAN,
            postcode TEXT,
            titel TEXT,
            prijs TEXT,
            link TEXT,
            data JSON,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW(),
            UNIQUE (bron, extern_id)
        );
    """)

    conn.commit()
    conn.close()

