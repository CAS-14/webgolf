CREATE TABLE blogposts(
    id INTEGER PRIMARY KEY NOT NULL,
    time INTEGER NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    comments INTEGER NOT NULL
);

CREATE TABLE comments(
    id INTEGER PRIMARY KEY NOT NULL,
    time INTEGER NOT NULL,
    parent INTEGER NOT NULL,
    author TEXT NOT NULL,
    body TEXT NOT NULL UNIQUE
);

CREATE TABLE artwork(
    id TEXT PRIMARY KEY NOT NULL,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    description TEXT NOT NULL
);