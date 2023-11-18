DROP TABLE IF EXISTS ingredients;

CREATE TABLE ingredients (  
   primary_id INTEGER PRIMARY KEY AUTO_INCREMENT,
   ingredient TEXT NOT NULL,  
   expiry INT,  
   amount INT,
);