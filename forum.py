import db
def get_pswdhash(username):
    sql = "SELECT password_hash FROM users WHERE username = ?"
    return db.query(sql, [username])[0][0]

def get_user_id(username):
    sql = "SELECT id FROM users WHERE username = ?"
    return db.query(sql, [username])[0][0]

def add_user(username, password_hash):
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])
    
def get_task(task_id):
    sql = "SELECT id, tila, task, body, user_id FROM tasks WHERE id = ?"
    result = db.query(sql, [task_id])
    return result[0] if result else None

def get_task_by_user(user_id):
    sql = "SELECT id, task FROM tasks WHERE user_id = ?"
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
    sql = "DELETE FROM comments WHERE task_id = ?"
    db.execute(sql, [task_id])
    sql = "DELETE FROM tasks WHERE id = ?"
    db.execute(sql, [task_id])

def add_comment(comment, task_id, user_id):
    sql = "INSERT INTO comments (body, task_id, user_id) VALUES (?, ?, ?)"
    db.execute(sql, [comment, task_id, user_id])

def get_comments(task_id):
    sql = "SELECT c.body, c.task_id, u.username FROM comments c, users u WHERE u.id = c.user_id AND c.task_id = ?"
    return db.query(sql, [task_id])

def search(query):
    sql = "SELECT id, task FROM tasks WHERE task LIKE ?"
    return db.query(sql, ["%" + query + "%"])