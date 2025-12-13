import sqlite3
from flask import g


def get_connection():
    con = sqlite3.connect("database.db", timeout = 5)
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con


def execute(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid
    con.close()
    return g.last_insert_id


def last_insert_id():
    return g.last_insert_id


def query(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    con.close()
    return result


def execute_many(sql, params=[]):
    con = get_connection()
    con.executemany(sql, params)
    con.commit()
    g.last_insert_id = con.execute("SELECT last_insert_rowid()").fetchone()[0]
    con.close()
