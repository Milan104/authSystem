# Login/Registration Program

This Python program allows a user to login or register, with the login details saved in a MySQL database.

## Prerequisites
1. Python 3
2. mysql-connector-python (can be installed using pip install mysql-connector-python)
3. A MySQL database and a table with columns for "id", "username", and "password" (the table can be created using the following SQL statement: CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL))

## Usage
To run the program, enter python client_auth.py in the terminal.

Follow the prompts to choose between login and registration. If you choose login, enter your username and password. If you choose registration, enter a new username and password.

## Acknowledgments
1. mysql-connector-python documentation: https://dev.mysql.com/doc/connector-python/en/
