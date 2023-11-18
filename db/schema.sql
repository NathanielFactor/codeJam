CREATE DATABASE ingredients;

DROP TABLE IF EXISTS ingredients;

CREATE TABLE ingredients (  
   id INT NOT NULL AUTO_INCREMENT,
   ingredient TEXT NOT NULL,  
   expiry INT,  
   amount INT,
   PRIMARY KEY ( id )  
);  