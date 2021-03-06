-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS messages;

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
  dt DATETIME NOT NULL,
  upvotes INTEGER NOT NULL,
  downvotes INTEGER NOT NULL
);

CREATE TABLE messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  userfrom TEXT NOT NULL,
  userto TEXT NOT NULL,
  messagecontent TEXT NOT NULL,
  flag BOOLEAN NOT NULL default 0,
  ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
