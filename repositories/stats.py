from todoapp import db

def task_count_all():
    sql = "SELECT COUNT(task) FROM tasks"
    result = db.query(sql)
    return result[0][0] if result else 0


def task_count_by_user(user_id):
    sql = "SELECT COUNT(task) FROM tasks WHERE user_id = ?"
    result = db.query(sql, [user_id])
    return result[0][0] if result else 0


def task_count_by_user_and_status(user_id, status):
    sql = "SELECT COUNT(task) FROM tasks WHERE user_id = ? AND task_status = ?"
    result = db.query(sql, [user_id, status])
    return result[0][0] if result else 0


def task_completed_count_by_user(user_id):
    sql = "SELECT COUNT(task) FROM tasks WHERE user_id = ? AND task_status = 1"
    result = db.query(sql, [user_id])
    return result[0][0] if result else 0


def comment_distinct_task_count(user_id):
    sql = "SELECT COUNT(DISTINCT task_id) FROM comments WHERE user_id = ?"
    result = db.query(sql, [user_id])
    return result[0][0] if result else 0


def comment_distinct_user_count(user_id):
    sql = """SELECT COUNT(DISTINCT t.user_id) FROM tasks t,comments c 
            WHERE t.id = c.task_id AND c.user_id = ?"""
    result = db.query(sql, [user_id])
    return result[0][0] if result else 0


def comment_count(task_id):
    sql = "SELECT COUNT(body) FROM comments WHERE task_id = ?"
    result = db.query(sql, [task_id])
    return result[0][0] if result else 0


def comment_count_by_user(user_id):
    sql = "SELECT COUNT(body) FROM comments WHERE user_id = ?"
    result = db.query(sql, [user_id])
    return result[0][0] if result else 0


def comment_sum_by_user(user_id):
    sql = "SELECT COUNT(c.body) FROM tasks t, comments c WHERE t.id = c.task_id AND t.user_id = ?"
    result = db.query(sql, [user_id])
    return result[0][0] if result else 0


def most_commented_task(user_id):
    sql = """SELECT t.task FROM tasks t, comments c WHERE t.id = c.task_id 
            AND t.user_id = ? GROUP BY t.task ORDER BY COUNT(c.task_id) DESC"""
    result = db.query(sql, [user_id])
    if result:
        return result[0][0]
    sql = "SELECT task FROM tasks WHERE user_id = ?"
    result = db.query(sql, [user_id])
    return result[0][0] if result else None


def popular_task_com_sum(user_id):
    sql = """SELECT COUNT(c.task_id) FROM tasks t, comments c WHERE t.id = c.task_id 
            AND t.user_id = ? GROUP BY t.task ORDER BY COUNT(c.task_id) DESC"""
    result = db.query(sql, [user_id])
    return result[0][0] if result else 0
