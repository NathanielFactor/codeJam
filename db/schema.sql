DROP TABLE IF EXISTS ingredients;

CREATE TABLE ingredients (
    ingredient TEXT NOT NULL,
    id INTEGER PRIMARY KEY,
	expiry_data TEXT NOT NULL,
	amount INTEGER PRIMARY KEY,
);  