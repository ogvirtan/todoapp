import db
def get_pswdhash(username):
    sql = "SELECT password_hash FROM users WHERE username = ?"
    return db.query(sql, [username])[0][0]

def add_user(username, password_hash):
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])
    
def get_task(task_id):
    sql = "SELECT * FROM tasks WHERE id = ?"
    return db.query(sql, [task_id])[0]

def get_task_by_user(user_id):
    sql = "SELECT * FROM tasks WHERE user_id = ?"
    return db.query(sql, [user_id])

def add_task(task, body, user_id):
    sql = "INSERT INTO tasks (tila, task, body, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [0, task, body, user_id])

def update_task(task_id, body):
    sql = "UPDATE tasks SET body = ? WHERE id = ?"
    db.execute(sql, [body, task_id])

def mark_task_done(task_id):
    sql = "UPDATE tasks SET tila = ? WHERE id = ?"
    db.execute(sql, [1 , task_id])

def remove_task(task_id):
    sql = "DELETE FROM tasks WHERE id = ?"
    db.execute(sql, [task_id])

def search(query):
    sql = """SELECT t.task,
                    t.body,
                    t.id,
                    u.username
             FROM tasks t, users u
             WHERE u.id = t.user_id AND
                   t.body LIKE ?"""
    return db.query(sql, ["%" + query + "%"])