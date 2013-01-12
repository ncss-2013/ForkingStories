CREATE TABLE IF NOT EXISTS users (
  id INTEGER NOT NULL,
  firstname TEXT NOT NULL,
  lastname TEXT NOT NULL,
  username TEXT NOT NULL,
  password TEXT NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS paragraph (
    id INTEGER NOT NULL,
    content TEXT NOT NULL,
    parent_id INT,
    votes INT NOT NULL,
    created TEXT NOT NULL,
    author_id INT NOT NULL,
    approved INT NOT NULL,
    story_id INT NOT NULL,
    PRIMARY KEY (id)
);


REPLACE INTO users VALUES (0, 'Barry', 'Schultz', 'barry_1233', '1234');
REPLACE INTO users VALUES (1, 'Prue', 'Robinson', 'prob_hi', '4682');
REPLACE INTO users VALUES (2, 'Andrew', 'Varvel', 'sdfko', 'password123');

REPLACE INTO paragraph VALUES (0, '"You shall not pass!"', 0, 10, '2013-01-12 10:54:51.404000', 2,
    0, 0);
REPLACE INTO paragraph VALUES (1, '"I totally SHALL pass!"', 0, 10, '2013-01-12 11:09:39.950000', 1,
    0, 0);
REPLACE INTO paragraph VALUES (2, 'Wizard Gandalf style!', 0, 10, '2013-01-12 11:11:08.043000', 0,
    0, 0);