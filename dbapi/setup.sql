CREATE TABLE IF NOT EXISTS users (
  id INTEGER NOT NULL,
  firstname TEXT NOT NULL,
  lastname TEXT NOT NULL,
  username TEXT NOT NULL,
  password TEXT NOT NULL,
  PRIMARY KEY (id)
);



REPLACE INTO users VALUES (0, 'Barry', 'Schultz', 'barry_1233', '1234');
REPLACE INTO users VALUES (1, 'Prue', 'Robinson', 'prob_hi', '4682');
REPLACE INTO users VALUES (2, 'Andrew', 'Varvel', 'sdfko', 'password123');
