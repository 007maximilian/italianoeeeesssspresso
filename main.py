import sys
import sqlite3
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QDialog, QMessageBox
from PyQt5.QtCore import Qt
from UI.main_ui import Ui_MainWindow
from UI.addEditCoffeeForm_ui import Ui_AddEditCoffeeForm

class AddEditCoffeeForm(QDialog, Ui_AddEditCoffeeForm):
    def __init__(self, parent=None, coffee_id=None):
        super().__init__(parent)
        self.setupUi(self)
        self.coffee_id = coffee_id
        
        if coffee_id:
            self.setWindowTitle('Edit Coffee')
            self.load_coffee_data()
        else:
            self.setWindowTitle('Add Coffee')
    
    def load_coffee_data(self):
        db_path = os.path.join(os.path.dirname(__file__), 'data', 'coffee.sqlite')
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM coffee WHERE id = ?', (self.coffee_id,))
        coffee = cursor.fetchone()
        connection.close()
        
        if coffee:
            self.nameEdit.setText(coffee[1])
            index = self.roastCombo.findText(coffee[2])
            self.roastCombo.setCurrentIndex(index)
            index = self.typeCombo.findText(coffee[3])
            self.typeCombo.setCurrentIndex(index)
            self.tasteEdit.setText(coffee[4])
            self.priceSpin.setValue(coffee[5])
            self.volumeSpin.setValue(coffee[6])
    
    def get_data(self):
        return (
            self.nameEdit.text(),
            self.roastCombo.currentText(),
            self.typeCombo.currentText(),
            self.tasteEdit.toPlainText(),
            self.priceSpin.value(),
            self.volumeSpin.value()
        )

class CoffeeWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.addButton.clicked.connect(self.add_coffee)
        self.editButton.clicked.connect(self.edit_coffee)
        self.deleteButton.clicked.connect(self.delete_coffee)
        self.refreshButton.clicked.connect(self.load_coffee_data)
        
        self.load_coffee_data()
    
    def get_db_path(self):
        return os.path.join(os.path.dirname(__file__), 'data', 'coffee.sqlite')
    
    def load_coffee_data(self):
        db_path = self.get_db_path()
        if not os.path.exists(db_path):
            QMessageBox.critical(self, 'Error', 'Database file not found!')
            return
            
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM coffee')
        data = cursor.fetchall()
        connection.close()
        
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'Name', 'Roast', 'Type', 'Taste', 'Price', 'Volume'])
        
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.tableWidget.setItem(i, j, item)
        
        self.tableWidget.resizeColumnsToContents()
    
    def add_coffee(self):
        dialog = AddEditCoffeeForm(self)
        if dialog.exec_():
            data = dialog.get_data()
            db_path = self.get_db_path()
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO coffee (name, roast_level, ground_or_beans, taste_description, price, package_volume)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', data)
            connection.commit()
            connection.close()
            self.load_coffee_data()
            QMessageBox.information(self, 'Success', 'Coffee added successfully!')
    
    def edit_coffee(self):
        current_row = self.tableWidget.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, 'Warning', 'Please select a coffee to edit')
            return
        
        coffee_id = int(self.tableWidget.item(current_row, 0).text())
        dialog = AddEditCoffeeForm(self, coffee_id)
        if dialog.exec_():
            data = dialog.get_data()
            db_path = self.get_db_path()
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            cursor.execute('''
                UPDATE coffee 
                SET name=?, roast_level=?, ground_or_beans=?, taste_description=?, price=?, package_volume=?
                WHERE id=?
            ''', (*data, coffee_id))
            connection.commit()
            connection.close()
            self.load_coffee_data()
            QMessageBox.information(self, 'Success', 'Coffee updated successfully!')
    
    def delete_coffee(self):
        current_row = self.tableWidget.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, 'Warning', 'Please select a coffee to delete')
            return
        
        coffee_id = int(self.tableWidget.item(current_row, 0).text())
        coffee_name = self.tableWidget.item(current_row, 1).text()
        
        reply = QMessageBox.question(self, 'Confirm Delete', 
                                    f'Are you sure you want to delete {coffee_name}?',
                                    QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            db_path = self.get_db_path()
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            cursor.execute('DELETE FROM coffee WHERE id = ?', (coffee_id,))
            connection.commit()
            connection.close()
            self.load_coffee_data()
            QMessageBox.information(self, 'Success', 'Coffee deleted successfully!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CoffeeWindow()
    window.show()
    sys.exit(app.exec_())
