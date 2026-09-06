import sqlite3
import time

from flask import g

time_queries = False

def get_connection():
    con = sqlite3.connect("database.db")
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con

def print_query_time(sql, start):
    elapsed = (time.perf_counter() - start) * 1000
    one_line = " ".join(sql.split())
    print(f"{elapsed:.1f} ms  {one_line}", flush=True)

def execute(sql, params=[]):
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
    return g.last_insert_id

def query(sql, params=[]):
    start = time.perf_counter()
    con = get_connection()
    try:
        result = con.execute(sql, params).fetchall()
    finally:
        con.close()
    if time_queries:
        print_query_time(sql, start)
    return result
