import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem

class CoffeeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.loadButton.clicked.connect(self.load_coffee_data)
        self.load_coffee_data()
    
    def load_coffee_data(self):
        connection = sqlite3.connect('coffee.sqlite')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM coffee')
        data = cursor.fetchall()
        connection.close()
        
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(7)
        
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(i, j, item)
        
        self.tableWidget.resizeColumnsToContents()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CoffeeWindow()
    window.show()
    sys.exit(app.exec_())
