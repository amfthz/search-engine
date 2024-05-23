USE amin_db_with_index;
CREATE TABLE IF NOT EXISTS wiki (
    id INT NOT NULL AUTO_INCREMENT,
    filename VARCHAR(255),
    full_path VARCHAR(255),
    file_size INT,
    last_modified DATETIME,
    content LONGTEXT,
    PRIMARY KEY (id)
);

SHOW TABLES;
select * from wiki;

-- Create an index on the filename column
CREATE INDEX idx_filename ON wiki(filename);

-- Create a full-text index on the content column
CREATE FULLTEXT INDEX idx_content ON wiki(content);
select * from wiki;
describe wiki;




