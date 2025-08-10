import psycopg2
from config import PG_CONN_STRING
from llm import get_embedding

def bm25_search(query, limit=5):
    with psycopg2.connect(PG_CONN_STRING) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT content FROM regulation_chunks ORDER BY content <-> %s LIMIT %s", (query, limit))
            return [row[0] for row in cur.fetchall()]

def semantic_search(query, limit=5):
    embedding = get_embedding(query)
    with psycopg2.connect(PG_CONN_STRING) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT content FROM regulation_chunks ORDER BY embedding <-> %s::vector LIMIT %s", (embedding, limit))
            return [row[0] for row in cur.fetchall()]
        
def vector_search(query, limit=5):
    emb = get_embedding(query)
    with psycopg2.connect(PG_CONN_STRING) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT content FROM regulation_chunks ORDER BY embedding <-> %s::vector LIMIT %s", (emb, limit))
            return [row[0] for row in cur.fetchall()]
