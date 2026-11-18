import os
import mysql.connector
from mysql.connector import pooling

_pool = None


def connection():
    global _pool
    if _pool is None:
        _pool = pooling.MySQLConnectionPool(
            pool_name="study_finder",
            pool_size=5,
            host=os.getenv("MYSQL_HOST", "127.0.0.1"),
            port=int(os.getenv("MYSQL_PORT", "3306")),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            database=os.getenv("MYSQL_DATABASE", "study_finder"),
        )
    return _pool.get_connection()


def query(sql, params=(), one=False):
    conn = connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(sql, params)
        return cursor.fetchone() if one else cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def execute(sql, params=()):
    conn = connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql, params)
        conn.commit()
        return cursor.lastrowid
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
