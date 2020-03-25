-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS posts;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  userName TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  karma INTEGER NOT NULL
);

CREATE TABLE posts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  community TEXT NOT NULL,
  text TEXT NOT NULL,
  Username TEXT NOT NULL,
  url TEXT,
  dt DATETIME NOT NULL
);
