import mysql.connector
import getpass
import socket
import uuid
from datetime import datetime


cnx = mysql.connector.connect(user='root', password='', host='localhost', database='users')
cursor = cnx.cursor()
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
        print("Key allready used or invalid!")
        
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
# use_key("obtxsfig", "huren")

print(subtime_left("devtest"))