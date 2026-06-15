# ============================================================
# utils/db_connection.py  –  MySQL connection pool
# ============================================================
import mysql.connector
from mysql.connector import pooling
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

_pool = None

def _get_pool():
    global _pool
    if _pool is None:
        _pool = pooling.MySQLConnectionPool(
            pool_name="lms_pool",
            pool_size=5,
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            autocommit=False
        )
    return _pool

def get_connection():
    """Return a connection from the pool."""
    return _get_pool().get_connection()

def execute_query(sql, params=None, fetch=True):
    """
    Execute a query and return results.
    For SELECT: returns list of dicts.
    For INSERT/UPDATE/DELETE: returns lastrowid or rowcount.

    FIX: cursor is now always closed in the finally block to prevent
    resource leaks when an exception is raised mid-query.
    """
    conn = get_connection()
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, params or ())
        if fetch:
            result = cursor.fetchall()
        else:
            conn.commit()
            result = cursor.lastrowid if cursor.lastrowid else cursor.rowcount
        return result
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        if cursor is not None:
            cursor.close()   # FIX: was missing — caused cursor leak on exception
        conn.close()
