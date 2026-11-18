CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    author_id INTEGER NOT NULL,
    created_at TEXT NOT NULL,  -- ISO-8601, second precision
    body TEXT NOT NULL
);
CREATE INDEX posts_created_at ON posts (created_at);
