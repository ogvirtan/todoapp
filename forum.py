import db
def get_pswdhash(username):
    sql = "SELECT password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    return result[0][0] if result else None

def get_user_id(username):
    sql = "SELECT id FROM users WHERE username = ?"
    return db.query(sql, [username])[0][0]

def get_username(user_id):
    sql = "SELECT username FROM users WHERE id = ?"
    return db.query(sql, [user_id])[0][0]

def add_user(username, password_hash):
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])
    
def get_task(task_id):
    sql = "SELECT id, tila, task, body, user_id FROM tasks WHERE id = ?"
    result = db.query(sql, [task_id])
    return result[0] if result else None

def get_task_by_user(user_id, page, page_size):
    sql = "SELECT id, task FROM tasks WHERE user_id = ? LIMIT ? OFFSET ?"
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [user_id, limit, offset])

def task_count_by_user(user_id):
    sql = "SELECT COUNT(task) FROM tasks WHERE user_id = ?"
    result = db.query(sql, [user_id])
    return result[0][0] if result else None

def task_completed_count_by_user(user_id):
    sql = "SELECT COUNT(task) FROM tasks WHERE user_id = ? AND tila = 1"
    result = db.query(sql, [user_id])
    return result[0][0] if result else 0

def comment_distinct_task_count(user_id):
    sql = "SELECT COUNT(DISTINCT task_id) FROM comments WHERE user_id = ?"
    result = db.query(sql, [user_id])
    return result[0][0] if result else 0

def comment_distinct_user_count(user_id):
    sql = "SELECT COUNT(DISTINCT t.user_id) FROM tasks t,comments c WHERE t.id = c.task_id AND c.user_id = ?"
    result = db.query(sql, [user_id])
    return result[0][0] if result else 0

def add_task(task, body, user_id):
    sql = "INSERT INTO tasks (tila, task, body, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [0, task, body, user_id])

def update_task(task, body, task_id):
    sql = "UPDATE tasks SET (task, body) = (?, ?) WHERE id = ?"
    db.execute(sql, [task, body, task_id])

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

def get_comments(task_id, page, page_size):
    sql = "SELECT c.body, c.task_id, u.username, u.id FROM comments c, users u WHERE u.id = c.user_id AND c.task_id = ? LIMIT ? OFFSET ?"
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [task_id, limit, offset])

def comment_count(task_id):
    sql = "SELECT COUNT(body) FROM comments WHERE task_id = ?"
    result = db.query(sql, [task_id])
    return result[0][0] if result else None

def comment_count_by_user(user_id):
    sql = "SELECT COUNT(body) FROM comments WHERE user_id = ?"
    result = db.query(sql, [user_id])
    return result[0][0] if result else 0

def comment_sum_by_user(user_id):
    sql = "SELECT COUNT(c.body) FROM tasks t, comments c WHERE t.id = c.task_id AND t.user_id = ?"
    result = db.query(sql, [user_id])
    return result[0][0] if result else 0

def most_commented_task(user_id):
    sql = "SELECT t.task FROM tasks t, comments c WHERE t.id = c.task_id AND t.user_id = ? GROUP BY t.task ORDER BY COUNT(c.task_id) DESC"
    result = db.query(sql, [user_id])
    if result:
        return result[0][0]
    else:
        sql = "SELECT task FROM tasks WHERE user_id = ?"
        result = db.query(sql, [user_id])
        return result[0][0] if result else None

def popular_task_com_sum(user_id):
    sql = "SELECT COUNT(c.task_id) FROM tasks t, comments c WHERE t.id = c.task_id AND t.user_id = ? GROUP BY t.task ORDER BY COUNT(c.task_id) DESC"
    result = db.query(sql, [user_id])
    return result[0][0] if result else 0

def search(query, page, page_size):
    sql = "SELECT id, task FROM tasks WHERE task LIKE ? LIMIT ? OFFSET ?"
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, ["%" + query + "%", limit, offset])

def search_count(query):
    sql = "SELECT COUNT(task) FROM tasks WHERE task LIKE ?"
    result = db.query(sql, ["%" + query + "%"])
    return result[0][0] if result else None