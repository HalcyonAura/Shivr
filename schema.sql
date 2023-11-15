DROP TABLE IF EXISTS sharks;

    CREATE TABLE if not exists sharks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age TEXT NOT NULL,
    gender INTEGER,
    weight INTEGER,
    length INTEGER,
    type TEXT,
    image TEXT,
    last_online TIMESTAMP CURRENT_TIMESTAMP
);