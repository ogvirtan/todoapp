CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    tila BOOLEAN,
    task TEXT,
    body TEXT,
    category_id INTEGER REFERENCES categories,
    user_id INTEGER REFERENCES users
);

CREATE INDEX idx_user_tasks ON tasks (user_id);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    title TEXT,
    user_id INTEGER REFERENCES users,
    UNIQUE (user_id, title)
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    body TEXT,
    task_id INTEGER REFERENCES tasks,
    user_id INTEGER REFERENCES users
);

CREATE INDEX idx_task_comments ON comments (task_id);
CREATE INDEX idx_user_comments ON comments (user_id);