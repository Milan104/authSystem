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
        
        # adding subtime to the user and setting the activation date
        query = "UPDATE users SET activation_date=%s, sub_length=%s WHERE username=%s"
        cursor.execute(query, (datetime.now(), key_duration, username)) # adding current date as activation date and sub lenght from the key
        cnx.commit()
    else:
        return False
        
        
def subtime_left(username):
    
    # checking the activation date
    query = "SELECT activation_date FROM users WHERE username=%s"
    cursor.execute(query, (username,))
    date_str = cursor.fetchone()[0]
    
    # handling the case of no activation date existing due to the user never having an active sub
    if date_str != '':
        date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f") # convert string to datetime object
    
        now = datetime.now()
        days_since = int((now - date).total_seconds() / 86400)
    
        # checking the sub_lenght
        query = "SELECT sub_length FROM users WHERE username=%s"
        cursor.execute(query, (username,))
        sub_lenght = cursor.fetchone()[0]
    
        # calulating the days left
        if days_since < int(sub_lenght):
            return f"You have {int(sub_lenght) - days_since} day/s left on your sub!"
        else:
            return False
    else:
        return False
    

# Prompt the user to choose between login and registration
while True:
    print("""
1.Login
2.Register
        """)
    choice = input("Would you like to login or register?: ")
    if choice == "1":
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
            
            # check if the user has a sub
            if subtime_left(username) == False:
                print("No active subscription!")
                
                # give option to enter a license
                key = input("Enter your key: ")
                
                # check if the key is valid
                if use_key(key, username) == False:
                    print("Key could not be activated. It may be invalid or allready in use!")
                    continue

            # Print a success message and allow the user to proceed
            print("Login successful!")
            break
        else:
            # If no match is found, print an error message and go back to the beginning of the loop
            print("Invalid username, password or hardware id. Please try again or contact our staff members.")
    elif choice == "2":
        # Prompt the user for a new username and password + the key
        username = input("Enter a new username: ")
        password = getpass.getpass("Enter a new password: ")
        key = input("Key: ")
        
        
        # check if the username allready exists
        query = "SELECT * FROM users WHERE username=%s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        if result:
            print("Username allready taken! Please choose an unique one!")
            continue
        # Insert the new username, password, and IP address into the database
        query = "INSERT INTO users (username, password, ip, hwid) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (username, password, ip, hwid()))
        cnx.commit()
        
        # check the given key and add it to the user
        if use_key(key, username) == False:
            print("Key could not be activated. It may be invalid or allready in use!")
            continue
        # Print a success message and allow the user to proceed
        print("Registration successful!")
        break
    else:
        # If the user enters an invalid choice, print an error message and go back to the beginning of the loop
        print("Invalid choice. Please enter '1'(login) or '2'(register).")

# Close the cursor and connection to the database
cursor.close()
cnx.close()