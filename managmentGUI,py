import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import mysql.connector
import random
import string

# creating a random string for the key
def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

# adding the keys to the database
def add_keys(number, lenght, duration):
    for x in range(number):
        query = "INSERT INTO keycodes (keycodes, status, duration) VALUES (%s, %s, %s)"
        cursor.execute(query, (get_random_string(lenght), "unused", duration))
        cnx.commit()

# connecting to the mysql database
cnx = mysql.connector.connect(user='root', password='', host='localhost', database='users')
cursor = cnx.cursor()

class KeyGenerationTool(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Create the input fields
        self.number_label = QtWidgets.QLabel('Number of Keys:')
        self.number_input = QtWidgets.QLineEdit()
        self.length_label = QtWidgets.QLabel('Key Length:')
        self.length_input = QtWidgets.QLineEdit()
        self.duration_label = QtWidgets.QLabel('Duration (days):')
        self.duration_input = QtWidgets.QLineEdit()
        
        # Create the generate button
        self.generate_button = QtWidgets.QPushButton('Generate Keys')
        self.generate_button.clicked.connect(self.generate_keys)

        # size
        self.setGeometry(0, 0, 300, 300)
        
        # Create the layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.number_label)
        layout.addWidget(self.number_input)
        layout.addWidget(self.length_label)
        layout.addWidget(self.length_input)
        layout.addWidget(self.duration_label)
        layout.addWidget(self.duration_input)
        layout.addWidget(self.generate_button)
        self.setLayout(layout)

        self.setWindowTitle('Key Generation Tool')
        self.show()

    def generate_keys(self):
        number = int(self.number_input.text())
        length = int(self.length_input.text())
        duration = int(self.duration_input.text())
        add_keys(number, length, duration)
        QtWidgets.QMessageBox.information(self, 'Success', 'Keys generated successfully!')
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    tool = KeyGenerationTool()
    sys.exit(app.exec_())