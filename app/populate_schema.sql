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
