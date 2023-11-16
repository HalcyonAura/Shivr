DROP TABLE IF EXISTS sharks;

    CREATE TABLE if not exists sharks (
    id INTEGER PRIMARY KEY,
    slug TEXT NOT NULL,
    name TEXT NOT NULL,
    age TEXT NOT NULL,
    gender INTEGER,
    weight TEXT,
    length TEXT,
    species TEXT,
    image TEXT,
    last_online TIMESTAMP CURRENT_TIMESTAMP,
    bio TEXT,
    lat REAL NOT NULL,
    long REAL NOT NULL
);