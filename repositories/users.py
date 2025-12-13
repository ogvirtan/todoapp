from todoapp import db

def get_pswdhash(username):
    sql = "SELECT password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    return result[0][0] if result else None


def get_user_id(username):
    sql = "SELECT id FROM users WHERE username = ?"
    result = db.query(sql, [username])
    return result[0][0] if result else None


def get_username(user_id):
    sql = "SELECT username FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0][0] if result else None


def add_user(username, password_hash):
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])