CREATE TABLE paragraph (
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