from todoapp import db

def get_task(task_id):
    sql = """SELECT t.id, t.task_status, t.task, t.body, t.user_id, u.username 
            FROM tasks t, users u WHERE t.user_id = u.id AND t.id = ?"""
    result = db.query(sql, [task_id])
    return result[0] if result else None


def get_tasks_by_user(user_id, page, page_size):
    sql = "SELECT id, task FROM tasks WHERE user_id = ? LIMIT ? OFFSET ?"
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [user_id, limit, offset])


def get_tasks_by_user_and_status(user_id, status, page, page_size):
    sql = "SELECT id, task FROM tasks WHERE user_id = ? AND task_status = ? LIMIT ? OFFSET ?"
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [user_id, status, limit, offset])


def get_all_tasks(page, page_size):
    sql = "SELECT id, task FROM tasks LIMIT ? OFFSET ?"
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [limit, offset])

def add_task(task, body, user_id, category_ids=[]):
    sql = "INSERT INTO tasks (task_status, task, body, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [0, task, body, user_id])
    task_id = db.last_insert_id()

    if category_ids:
        rows = [(task_id, cid) for cid in category_ids]
        db.execute_many("INSERT INTO task_categories (task_id, category_id) VALUES (?, ?)", rows)

    return task_id


def update_task(task, body, task_id, category_ids=None):
    if category_ids is None:
        category_ids = []
        
    sql = "UPDATE tasks SET task = ?, body = ? WHERE id = ?"
    db.execute(sql, [task, body, task_id])

    sql_delete = "DELETE FROM task_categories WHERE task_id = ?"
    db.execute(sql_delete, [task_id])

    if category_ids:
        rows = [(task_id, cid) for cid in category_ids]
        db.execute_many("INSERT INTO task_categories (task_id, category_id) VALUES (?, ?)", rows)

def set_task_status(task_id, status):
    sql = "UPDATE tasks SET task_status = ? WHERE id = ?"
    db.execute(sql, [status, task_id])


def remove_task(task_id):
    sql = "DELETE FROM comments WHERE task_id = ?"
    db.execute(sql, [task_id])
    sql = "DELETE FROM tasks WHERE id = ?"
    db.execute(sql, [task_id])
    sql = "DELETE FROM task_categories WHERE task_id = ?"
    db.execute(sql, [task_id])

def search(query, page, page_size):
    sql = "SELECT id, task FROM tasks WHERE task LIKE ? LIMIT ? OFFSET ?"
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, ["%" + query + "%", limit, offset])


def search_count(query):
    sql = "SELECT COUNT(task) FROM tasks WHERE task LIKE ?"
    result = db.query(sql, ["%" + query + "%"])
    return result[0][0] if result else None