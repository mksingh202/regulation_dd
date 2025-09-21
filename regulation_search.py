import psycopg2
from config import PG_CONN_STRING
from llm import get_embedding


class RegulationSearch:
    def __init__(self, conn_string=PG_CONN_STRING):
        self.conn_string = conn_string

    def _execute_query(self, query, params):
        """Helper to execute SQL queries and fetch results."""
        with psycopg2.connect(self.conn_string) as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return [row[0] for row in cur.fetchall()]

    def bm25_search(self, query, limit=5):
        sql = """
            SELECT content 
            FROM regulation_chunks 
            ORDER BY content <-> %s 
            LIMIT %s
        """
        return self._execute_query(sql, (query, limit))

    def vector_search(self, query, limit=5):
        embedding = get_embedding(query)
        sql = """
            SELECT content 
            FROM regulation_chunks 
            ORDER BY embedding <-> %s::vector 
            LIMIT %s
        """
        return self._execute_query(sql, (embedding, limit))
