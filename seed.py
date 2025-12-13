import random
import sqlite3

db = sqlite3.connect("database.db")
cur = db.cursor()

cur.execute("DELETE FROM users")
cur.execute("DELETE FROM tasks")
cur.execute("DELETE FROM categories")
cur.execute("DELETE FROM task_categories")
cur.execute("DELETE FROM comments")

db.commit()

user_count = 1000
task_count = 10**6
message_count = 10**7

users = [("user" + str(i),) for i in range(1, user_count + 1)]
cur.executemany("INSERT INTO users (username) VALUES (?)", users)

categories = ["tärkeä", "kriittinen", "vapaaehtoinen", "työ", "askare"]
category_rows = [(i, cat) for i in range(1, user_count + 1) for cat in categories]
cur.executemany("INSERT INTO categories (user_id, title) VALUES (?, ?)", category_rows)

for i in range(1, task_count + 1):
    user_id = random.randint(1, user_count)
    status = random.randint(0, 1)
    if random.random() < 0.25:
        category_id = None
    else:
        category_id = random.randint(1, len(categories))
        
    cur.execute("INSERT INTO tasks (task_status, task, body, user_id) VALUES (?, ?, ?, ?)",
               [status, "task" + str(i), "body", user_id])

    task_id = cur.lastrowid
    if category_id:
        cur.execute("INSERT INTO task_categories (task_id, category_id) VALUES (?, ?)", [task_id, category_id])

db.commit()

for i in range(1, message_count + 1):
    user_id = random.randint(1, user_count)
    task_id = random.randint(1, task_count)
    cur.execute("""INSERT INTO comments (body, task_id, user_id)
                  VALUES (?, ?, ?)""",
               ["message" + str(i), task_id, user_id])

db.commit()
db.close()
