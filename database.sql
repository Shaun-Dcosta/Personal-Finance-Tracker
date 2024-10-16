create database pft;
use pft;
create table user(
	user_id int primary key not null auto_increment,
    username varchar(30) not null,
    password varchar(30) not null,
    email varchar(30) not null check(email like"%@%.com")
);
create table accounts(
    acc_number VARCHAR(16) PRIMARY KEY CHECK (LENGTH(acc_number) BETWEEN 11 AND 16) not null,
    type ENUM('current', 'savings', 'fixed deposit', 'salary', 'nri', 'recurring deposit') not null,
    balance INT,
    doc DATE not null,
    min_balance INT,
    user_id INT not null,
    FOREIGN KEY (user_id) REFERENCES user(user_id) on delete cascade
);
create table transactions(
	transaction_id int primary key auto_increment not null,
	category enum('groceries','electricity','water','clothes','other') not null default 'other',
	amount int not null,
	recepient varchar(100) not null,
	timetstamp timestamp,
    user_id int not null,
    acc_number VARCHAR(16),
    foreign key (user_id) references user(user_id) on delete cascade,
    foreign key(acc_number) references accounts(acc_number) on delete set null
);
 create table budgets(
	budget_id int primary key auto_increment not null,
    amount int not null default 0,
    category enum('groceries','electricity','water','clothes','other') not null default 'other',
    amount_remaining int not null,
    user_id int not null,
    foreign key(user_id) references user(user_id) on delete cascade
);
create table income(
	income_id int primary key not null auto_increment,
    type enum('earned','capital gains','rental','passive','pension','commissions','other') not null default 'other',
    amount int not null,
    timetstamp timestamp not null,
    user_id int not null,
    acc_number VARCHAR(16),
    foreign key (user_id) references user(user_id) on delete cascade,
    foreign key(acc_number) references accounts(acc_number) on delete set null
);
create table debts(
	debt_id int primary key not null auto_increment,
    type enum('loans','credit card','mortgage'),
    amount int not null,
    due_date date,
    status enum('completed','due'),
    user_id int not null,
    foreign key (user_id) references user(user_id) on delete cascade
);
create table goals(
	goal_id int primary key not null auto_increment,
    type varchar(30) not null,
    target int not null,
    amount_saved int not null,
    status enum('reached','in progress') not null,
    doc date,
    target_date date,
    user_id int not null,
    foreign key (user_id) references user(user_id) on delete cascade
);
    
    
 