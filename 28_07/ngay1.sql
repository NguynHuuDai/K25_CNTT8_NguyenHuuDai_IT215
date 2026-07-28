CREATE DATABASE bai_tap_he_28_7;
use bai_tap_he_28_7;

create table students(
	id int auto_increment primary key,
    name varchar(50) not null,
    email varchar(50) not null,
    age int not null
)