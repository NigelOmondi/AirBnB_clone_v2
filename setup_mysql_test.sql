-- A script that prepares a MySQL server for the AirBnB project.
-- A database hbnb_test_db
-- A new user hbnb_test (in localhost)
-- The password of hbnb_test should be set to hbnb_test_pwd

-- The user -> hbnb_test should have all privileges on the
-- database hbnb_test_db ONLY.

-- The user -> hbnb_test should have SELECT privilege on the
-- database performance_schema (and only this database

-- If the database hbnb_test_db or the user hbnb_test already exists,
-- your script should not fail.

CREATE DATABASE IF NOT EXISTS hbnb_test_db;
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
GRANT ALL PRIVILEGES ON hbtn_test_db.* TO 'hbnb_test'@'localhost';
GRANT SELECT ON perfomance_schema.* TO 'hbnb_test'@'localhost';
FLUSH PRIVILEGES;
