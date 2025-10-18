import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM tasks")
db.execute("DELETE FROM comments")

user_count = 1000
task_count = 10**6
message_count = 10**7

for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username) VALUES (?)",
               ["user" + str(i)])

for i in range(1, task_count + 1):
    user_id = random.randint(1, user_count)
    status = random.randint(0,1)
    db.execute("INSERT INTO tasks (tila, task, body, user_id) VALUES (?, ?, ?, ?)",
               [status,"task" + str(i), "body", user_id])

for i in range(1, message_count + 1):
    user_id = random.randint(1, user_count)
    task_id = random.randint(1, task_count)
    db.execute("""INSERT INTO comments (body, task_id, user_id)
                  VALUES (?, ?, ?)""",
               ["message" + str(i), task_id, user_id])

db.commit()
db.close()