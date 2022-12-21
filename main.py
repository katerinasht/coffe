import sqlite3
import sys
from PyQt5.QtCore import Qt
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox, QInputDialog, QMainWindow, QTableWidgetItem



class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.update_result()
        self.modified = {}
        self.titles = None

    def update_result(self):
        cur = self.con.cursor()
        zapr = "SELECT * FROM coffee"
        self.result = cur.execute(zapr).fetchall()
        self.tableWidget.setRowCount(len(self.result))
        self.tableWidget.setColumnCount(len(self.result[0]))
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(self.result):
            for j, val in enumerate(elem):
                item = QTableWidgetItem(str(val))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.tableWidget.setItem(i, j, QTableWidgetItem(item))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())