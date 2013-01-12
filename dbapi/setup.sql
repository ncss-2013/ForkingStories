CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  fname TEXT NOT NULL,
  lname TEXT NOT NULL,
  username TEXT NOT NULL,
  password TEXT NOT NULL,
  dob TEXT NOT NULL,
  email TEXT NOT NULL,
  joindate REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS paragraph (
    id INTEGER NOT NULL,
    content TEXT NOT NULL,
    parent_id INT,
    votes INT NOT NULL,
    author_id INT NOT NULL,
    approved INT NOT NULL,
    story_id INT NOT NULL,
    created REAL NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS stories (
    id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    created_time REAL NOT NULL,
    PRIMARY KEY (id)
);

REPLACE INTO users VALUES (0, 'Barry', 'Schultz', 'barry_1233', '1234', '22/22/22', 'barry.sucks@gmail.com', 2.9);

REPLACE INTO paragraph VALUES (0, '"You shall not pass!"', NULL, 10, 2,
    0, 0, 1357962807.106);
REPLACE INTO paragraph VALUES (1, '"But you can dance!"', 0, 10,  1,
    0, 0, 1357962831.219);
REPLACE INTO paragraph VALUES (2, 'Wizard Gandalf style!', 1, 10, 0,
    0, 0, 1357962841.213);
