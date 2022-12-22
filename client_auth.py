import mysql.connector
import getpass
import socket
import uuid
from datetime import datetime

# Connect to the MySQL database
cnx = mysql.connector.connect(user='root', password='', host='localhost', database='users')
cursor = cnx.cursor()


# get the clients IP
ip = socket.gethostbyname(socket.gethostname())

# get the clients HWID
def hwid():
    mac_int = uuid.getnode()
    return hex(mac_int)[2:]

def use_key(keycode, username):
    # checking if the key exists and is unused
    query = "SELECT * FROM keycodes WHERE keycodes=%s AND status=%s"
    cursor.execute(query, (keycode, "unused"))
    result = cursor.fetchone()
    if result:
        # updating the status to used
        query = "UPDATE keycodes SET status=%s WHERE keycodes=%s"
        cursor.execute(query, ("used", keycode))
        cnx.commit()
        
        # checking the duration of the entered key
        query = "SELECT duration FROM keycodes WHERE keycodes=%s"
        cursor.execute(query, (keycode,))
        key_duration = cursor.fetchone()[0]
        print(key_duration)
        
        # adding subtime to the user and setting the activation date
        query = "UPDATE users SET activation_date=%s, sub_length=%s WHERE username=%s"
        cursor.execute(query, (datetime.now(), key_duration, username)) # adding current date as activation date and sub lenght from the key
        cnx.commit()
    else:
        print("Key allready used or invalid!")
        
# Prompt the user to choose between login and registration
while True:
    choice = input("Would you like to login or register? (login/register): ")
    if choice == "login":
        # Prompt the user for their username and password
        username = input("Enter your username: ")
        password = getpass.getpass("Enter your password: ")

        # Check if the provided username and password match any records in the database
        query = "SELECT * FROM users WHERE username=%s AND password=%s AND hwid=%s"
        cursor.execute(query, (username, password, hwid()))
        result = cursor.fetchone()
        if result:
            # If a match is found, update the user's IP address in the database
            query = "UPDATE users SET ip=%s WHERE username=%s"
            cursor.execute(query, (ip, username))
            cnx.commit()
            # Print a success message and allow the user to proceed
            print("Login successful!")
            break
        else:
            # If no match is found, print an error message and go back to the beginning of the loop
            print("Invalid username, password or hardware id. Please try again or contact our staff members.")
    elif choice == "register":
        # Prompt the user for a new username and password + the key
        username = input("Enter a new username: ")
        password = getpass.getpass("Enter a new password: ")
        key = input("Key: ")
        # Insert the new username, password, and IP address into the database
        query = "INSERT INTO users (username, password, ip, hwid) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (username, password, ip, hwid()))
        cnx.commit()
        
        # Print a success message and allow the user to proceed
        print("Registration successful!")
        break
    else:
        # If the user enters an invalid choice, print an error message and go back to the beginning of the loop
        print("Invalid choice. Please enter 'login' or 'register'.")

# Close the cursor and connection to the database
cursor.close()
cnx.close()