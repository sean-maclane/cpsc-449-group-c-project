DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS community;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS vote;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  user_pwd TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  karma INTEGER NOT NULL
);

CREATE TABLE community (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  community_name TEXT UNIQUE NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  author_id INTEGER NOT NULL,
  community_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (community_id) REFERENCES community (id)
);

CREATE TABLE vote (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  upvote INTEGER NOT NULL,
  downvote INTEGER NOT NULL
);

COMMIT;


-- Testing SQLite3 with dummy data:

insert into user(username, user_pwd, email, karma) values ('saurabh', 'saurabh123', 'saurabh@csu.fullerton.edu', 1);
insert into user(username, user_pwd, email, karma) values ('preston', 'preston123', 'preston@csu.fullerton.edu', 1);
insert into user(username, user_pwd, email, karma) values ('sean', 'sean123', 'sean@csu.fullerton.edu', 1);


INSERT INTO community(community_name) VALUES('news');
INSERT INTO community(community_name) VALUES('science');
INSERT INTO community(community_name) VALUES('movies');


INSERT INTO post(community_id, author_id, title, body) values (
(SELECT id FROM community WHERE community_name = 'news'),
(SELECT id FROM user WHERE username = 'saurabh'),
'News Headlines', 'news test body 123456789');

INSERT INTO post(community_id, author_id, title, body) values (
(SELECT id FROM community WHERE community_name = 'science'),
(SELECT id FROM user WHERE username = 'preston'),
'Scientific Innovations', 'science test body');

INSERT INTO post(community_id, author_id, title, body) values (
(SELECT id FROM community WHERE community_name = 'movies'),
(SELECT id FROM user WHERE username = 'sean'),
'1917 by Sam Mendes', 'movies test body 1234');

COMMIT;
