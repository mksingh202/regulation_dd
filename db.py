import psycopg2
from config import PG_CONN_STRING
from psycopg2.extras import execute_batch

def init_db():
    with psycopg2.connect(PG_CONN_STRING) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS regulation_chunks (
                    id SERIAL PRIMARY KEY,
                    content TEXT,
                    embedding VECTOR(768)
                );
            """)
            cur.execute("CREATE INDEX IF NOT EXISTS idx_chunk_bm25 ON regulation_chunks USING ivfflat (embedding vector_cosine_ops);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_content_bm25 ON regulation_chunks USING pgroonga (content);")
        conn.commit()

def insert_chunks(chunks, embeddings):
    with psycopg2.connect(PG_CONN_STRING) as conn:
        with conn.cursor() as cur:
            execute_batch(cur, """
                INSERT INTO regulation_chunks (content, embedding) VALUES (%s, %s)
            """, list(zip(chunks, embeddings)))
        conn.commit()
