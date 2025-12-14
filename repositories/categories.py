from todoapp import db

def add_category(title, user_id):
    sql = "INSERT INTO categories (title, user_id) VALUES (?, ?)"
    db.execute(sql, [title, user_id])

def get_categories_by_user(user_id):
    sql = "SELECT title FROM categories WHERE user_id = ?"
    titles = db.query(sql, [user_id])
    categories = [row[0] for row in titles]
    return categories if categories else []

def get_category_by_title_and_user(title , user_id):
    sql = "SELECT title FROM categories WHERE title = ? AND user_id = ?"
    result = db.query(sql, [title, user_id])
    return result[0][0] if result else None

def get_categories_by_task(task_id):
    sql = "SELECT c.title FROM categories c JOIN task_categories tc ON c.id = tc.category_id WHERE tc.task_id = ?"
    result = db.query(sql, [task_id])
    return [row[0] for row in result] if result else []

def get_category_ids(titles, user_id):
    if not titles:
        return []
    sql = "SELECT id FROM categories WHERE user_id = ? AND (" + " OR ".join("title = ?" for _ in titles) + ")"
    result = db.query(sql, [user_id] + titles)
    return [row[0] for row in result]