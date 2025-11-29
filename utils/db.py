import os
import psycopg2
from psycopg2.extras import RealDictCursor, Json

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


# ==============================================
# 🧩 Universally used by ALL scrapers
# ==============================================

def save_property(bron, extern_id, type_mode, postcode, titel, prijs, link, data, particulier=False):
    """
    Slaat een pand op. Indien bron + extern_id al bestaan → update ipv dubbele insert.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO panden (bron, extern_id, type, particulier, postcode, titel, prijs, link, data)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (bron, extern_id)
        DO UPDATE SET
            titel = EXCLUDED.titel,
            prijs = EXCLUDED.prijs,
            link = EXCLUDED.link,
            data = EXCLUDED.data,
            updated_at = NOW();
    """, (bron, extern_id, type_mode, particulier, postcode, titel, prijs, link, Json(data)))

    conn.commit()
    conn.close()
