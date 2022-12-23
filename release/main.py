import sqlite3
import sys
from PyQt5.QtCore import Qt
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox, QInputDialog
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from main1 import Ui_MainWindow
from addEditCoffeeForm import Ui_MainWindow as addEditCoffeeForm


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    text += ''.join(traceback.format_tb(tb))
    print(text)
    QtWidgets.QMessageBox.critical(None, 'Error', text)
    sys.exit()
sys.excepthook = log_uncaught_exceptions


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("data\coffee.sqlite")
        self.update_result()
        self.modified = {}
        self.titles = None
        self.pushButton.clicked.connect(self.add_result)
        self.pushButton_2.clicked.connect(self.edit_result)
        self.tableWidget.itemClicked.connect(self.item_clicked)

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

    def item_clicked(self, item):
        self.row = int(self.tableWidget.model().index(item.row(), 0).data()) - 1

    def adding(self, parametrs):
        cur = self.con.cursor()
        if self.ask.lineEdit.text() != '' and self.ask.lineEdit_2.text() != '' and self.ask.lineEdit_3.text() != '' and self.ask.lineEdit_4.text() != '' and self.ask.lineEdit_5.text() != '':
            cur.execute("INSERT INTO coffee('название сорта', 'степень обжарки', 'молотый/в зернах', 'описание вкуса', 'цена', 'объем упаковки') VALUES(?,?,?,?,?,?)",
                        (parametrs[0], parametrs[1], parametrs[2], parametrs[3], parametrs[4], parametrs[5]))
            self.update_result()
            self.ask.hide()
        else:
            self.bad(self.ask.label_7)
        self.con.commit()
        self.modified.clear()

    def bad(self, where):
        where.setText('неверно заполнена форма')

    def add_result(self):
        self.ask = asking()
        self.ask.show()
        self.ask.pushButton_2.clicked.connect(lambda: self.adding((self.ask.lineEdit.text(), self.ask.lineEdit_2.text(),
                                                                   self.ask.comboBox.currentText(),
                                                                   self.ask.lineEdit_3.text(),
                                                                   self.ask.lineEdit_4.text(),
                                                                   self.ask.lineEdit_5.text())))

    def edit_result(self):
        self.edt = editing(self.con.cursor(), str(int(self.row) + 1))
        self.edt.show()
        self.edt.pushButton_2.clicked.connect(lambda: self.editing((self.edt.lineEdit.text(), self.edt.lineEdit_2.text(),
                                                                   self.edt.comboBox.currentText(),
                                                                   self.edt.lineEdit_3.text(),
                                                                   self.edt.lineEdit_4.text(),
                                                                   self.edt.lineEdit_5.text())))

    def editing(self, parametrs):
        cur = self.con.cursor()
        if self.edt.lineEdit.text() != '' and self.edt.lineEdit_2.text() != '' and self.edt.lineEdit_3.text() != '' and self.edt.lineEdit_4.text() != '' and self.edt.lineEdit_5.text() != '':
            cur.execute("UPDATE coffee SET 'название сорта' = ?, 'степень обжарки' = ?, 'молотый/в зернах' = ?, 'описание вкуса' = ?, 'цена' = ?, 'объем упаковки' = ? WHERE id = ?", (parametrs[0], parametrs[1], parametrs[2], parametrs[3], parametrs[4], parametrs[5], str(int(self.row) + 1)))
            self.update_result()
            self.edt.hide()
        else:
            self.bad(self.edt.label_7)
        self.con.commit()
        self.modified.clear()


class asking(QMainWindow, addEditCoffeeForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class editing(QMainWindow, addEditCoffeeForm):
    def __init__(self, cur, row):
        super().__init__()
        self.setupUi(self)
        zapr = "SELECT * FROM coffee WHERE id = ?"
        edt = cur.execute(zapr, (row,)).fetchall()
        self.lineEdit.setText(edt[0][1])
        self.lineEdit_2.setText(str(edt[0][2]))
        if str(edt[0][3]) == 'молотый':
            self.comboBox.ListIndex = 0
        else:
            self.comboBox.ListIndex = 1
        self.lineEdit_3.setText(str(edt[0][4]))
        self.lineEdit_4.setText(str(edt[0][5]))
        self.lineEdit_5.setText(str(edt[0][6]))





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())

