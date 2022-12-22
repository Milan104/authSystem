import mysql.connector
import random
import string

# creating a random string for the key
def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

# connecting to the mysql database
cnx = mysql.connector.connect(user='root', password='', host='localhost', database='users')
cursor = cnx.cursor()




def add_keys(number, lenght, duration):
    for x in range(number):
        query = "INSERT INTO keycodes (keycodes, status, duration) VALUES (%s, %s, %s)"
        cursor.execute(query, (get_random_string(lenght), "unused", duration))
        cnx.commit()

if __name__ == '__main__':
    print("Key generation Tool...")
    number = int(input("Number of Keys to be generated: "))
    lenght = int(input("Letter lenght of the key: "))
    duration = (int(input("Duration in days of the keys: ")))
    add_keys(number, lenght, duration)