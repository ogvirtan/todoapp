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
    user_id INTEGER REFERENCES users
);

CREATE TABLE groups (
    id INTEGER PRIMARY KEY,
    task_id INTEGER REFERENCES tasks
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    body TEXT,
    task_id INTEGER REFERENCES tasks
);