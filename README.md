# Login/Registration Program with licensing and hardware lock

This Python program allows a user to login or register, with the login details saved in a MySQL database. The user also has to provide a key and their user account is locked to their machine. The keys/licenses can also be set to only last a specific time.

## Prerequisites
1. Python 3
2. mysql-connector-python (can be installed using pip install mysql-connector-python)
3. A MySQL database and a table with columns for "id", "username", "password", "ip", "hwid", "activation_date" and "sub_length" (the table can be created using the following SQL statement): 

```
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  ip VARCHAR(255) NOT NULL,
  hwid VARCHAR(255) NOT NULL,
  activation_date VARCHAR(255) NOT NULL,
  sub_length VARCHAR(255) NOT NULL,
); 
```
4. Another MySQL table with the keys the users could use. It should have the following columns: "id", "keycodes", "status" and "duration"
(the table can be created using the following SQL statement): 

```
CREATE TABLE keycodes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  keycodes VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  duration VARCHAR(255) NOT NULL
);
```

## Usage
To run the program, enter python client_auth.py in the terminal.
Follow the prompts to choose between login and registration. If you choose login, enter your username and password. If you choose registration, enter a new username and password.


### Files
#### auth_client.py
The main script to be run by the user managing the auth.
#### managment.py
For adding new keys with specific details to the database, which can be redeemed later.
#### managmentGUI.py
Same as managment.py but with a gui.
#### test.py
just for testing single functions and requests.


## Acknowledgments
1. mysql-connector-python documentation: https://dev.mysql.com/doc/connector-python/en/
