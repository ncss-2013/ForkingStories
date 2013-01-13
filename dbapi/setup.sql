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
REPLACE INTO paragraphs (id, content, parent_id, votes, author_id, approved, story_id, created) 
    VALUES (3, 'Wizard Gandalf style 2!', 1, 10, 0, 1, 0, "2013-01-13 14:24:27.000000");
REPLACE INTO paragraphs (id, content, parent_id, votes, author_id, approved, story_id, created) 
    VALUES (4, "It's a cave troll! Save the hobbits!", 0, 10, 0, 1, 0, "2013-01-13 16:24:27.000000");
REPLACE INTO paragraphs (id, content, parent_id, votes, author_id, approved, story_id, created) 
    VALUES (5, "Aragorn!", 2, 10, 0, 1, 0, "2013-01-13 16:24:27.000000");
REPLACE INTO stories (id,  author_id, title, created_time, author_init_comment, votes)
    VALUES (0, 0, "Wizard Gandalf Style", "2013-01-13 13:14:27.044000", "Comment", 0);

REPLACE INTO rules (id, story_id, rule_def_id, params)
    VALUES (0, 0, 1, "0||6");
REPLACE INTO rules (id, story_id, rule_def_id, params)
    VALUES (1, 0, 2, "cat||dog");
    
REPLACE INTO ruleDefs (id, name, description)
    VALUES (0, "forced_words", "User's text must include the words host submits");
REPLACE INTO ruleDefs (id, name, description)
    VALUES (1, "letters_per_word", "Returns False if the word is not within (or equal to) the minimum or maximum values set by the user.");
REPLACE INTO ruleDefs (id, name, description)
    VALUES (2, "banned_words", "Returns False if a banned word is found within the text.");
REPLACE INTO ruleDefs (id, name, description)
    VALUES (3, "max_num_words", "The number of words in submission must be <= host's input");
REPLACE INTO ruleDefs (id, name, description)
    VALUES (4, "include_number_words", "host sets requirement for certain word to be used in writers submission every ___ words");
