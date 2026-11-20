"""Database helpers for opening connections and running SQL queries."""

import sqlite3
import time

from flask import g

time_queries = False

def get_connection():
    """Open a database connection with foreign keys enabled."""
    con = sqlite3.connect("database.db")
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con

def print_query_time(sql, start):
    """Print the execution time of an SQL query."""
    elapsed = (time.perf_counter() - start) * 1000
    one_line = " ".join(sql.split())
    print(f"{elapsed:.1f} ms  {one_line}", flush=True)

def execute(sql, params=None):
    """Execute an SQL statement and commit the transaction."""
    if params is None:
        params = []
    start = time.perf_counter()
    con = get_connection()
    try:
        result = con.execute(sql, params)
        con.commit()
        g.last_insert_id = result.lastrowid
    finally:
        con.close()
    if time_queries:
        print_query_time(sql, start)

def last_insert_id():
    """Return the row ID created by the latest INSERT."""
    return g.last_insert_id

def query(sql, params=None):
    """Execute an SQL query and return all result rows."""
    if params is None:
        params = []
    start = time.perf_counter()
    con = get_connection()
    try:
        result = con.execute(sql, params).fetchall()
    finally:
        con.close()
    if time_queries:
        print_query_time(sql, start)
    return result
