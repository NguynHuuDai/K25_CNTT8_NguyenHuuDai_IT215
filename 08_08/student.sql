CREATE DATABASE IF NOT EXISTS student_management;

USE student_management;

CREATE TABLE IF NOT EXISTS students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    age INT NOT NULL,
    score FLOAT NOT NULL
);

INSERT INTO students (name, email, age, score)
VALUES
('Nguyen Van A', 'a@gmail.com', 20, 8.5),
('Tran Van B', 'b@gmail.com', 21, 7.5),
('Le Van C', 'c@gmail.com', 19, 9.0),
('Pham Van D', 'd@gmail.com', 22, 6.5),
('Hoang Van E', 'e@gmail.com', 20, 8.0);