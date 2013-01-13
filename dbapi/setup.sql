CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  fname TEXT NOT NULL,
  lname TEXT NOT NULL,
  username TEXT NOT NULL,
  password TEXT NOT NULL,
  dob TEXT NOT NULL,
  email TEXT NOT NULL,
  joindate TEXT NOT NULL,
  location TEXT NOT NULL,
  bio TEXT
);

CREATE TABLE IF NOT EXISTS paragraphs (
    id INTEGER NOT NULL,
    content TEXT NOT NULL,
    parent_id INT,
    votes INT NOT NULL,
    author_id INT NOT NULL,
    approved INT NOT NULL,
    story_id INT NOT NULL,
    created TEXT NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS stories (
    id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    created_time TEXT NOT NULL,
    author_init_comment TEXT NOT NULL,
    votes INTEGER NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS rules (
    id INTEGER NOT NULL,
    story_id INTEGER NOT NULL,
    rule_def_id INTEGER NOT NULL,
    params TEXT NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS ruleDefs (
    id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS comments (
    id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    story_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_time TEXT NOT NULL,
    PRIMARY KEY (id)
) ;

REPLACE INTO users (id, fname, lname, username, password, dob, email, joindate, location, bio)
    VALUES (0, 'Barry', 'Schultz', 'barry_1233', '1234', "2000-11-16 00:00:00.00000",
    'barry.sucks@gmail.com', "2000-11-16 00:00:00.00000", 'Sydney', "Hi, I'm Barry!");

REPLACE INTO paragraphs (id, content, parent_id, votes, author_id, approved, story_id, created) 
    VALUES (0, '"You shall not pass!"', -1, 10, 0, 1, 0, "2013-01-13 14:13:29.324000");
REPLACE INTO paragraphs (id, content, parent_id, votes, author_id, approved, story_id, created) 
    VALUES (1, '"But you can dance!"', 0, 10,  0, 1, 0, "2013-01-13 14:14:09.884000");
REPLACE INTO paragraphs (id, content, parent_id, votes, author_id, approved, story_id, created) 
    VALUES (2, 'Wizard Gandalf style!', 1, 10, 0, 1, 0, "2013-01-13 14:14:27.044000");
REPLACE INTO stories (id,  author_id, title, created_time, author_init_comment, votes)
    VALUES (0, 0, "This is such a cool story", "2013-01-13 13:14:27.044000", "Comment", 0);