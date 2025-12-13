from todoapp import db

def add_comment(comment, task_id, user_id):
    sql = "INSERT INTO comments (body, task_id, user_id) VALUES (?, ?, ?)"
    db.execute(sql, [comment, task_id, user_id])


def get_comments(task_id, page, page_size):
    sql = """SELECT c.body, c.task_id, u.username, u.id FROM comments c, users u 
            WHERE u.id = c.user_id AND c.task_id = ? LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [task_id, limit, offset])


def get_comments_by_user(user_id, page, page_size):
    sql = """SELECT c.body, c.task_id, t.task FROM comments c, users u, tasks t 
            WHERE u.id = ? AND u.id = c.user_id AND c.task_id = t.id LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [user_id, limit, offset])