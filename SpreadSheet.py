import sys
import os
import csv
from PyQt5.QtWidgets import QTableWidget, QApplication, QMainWindow, QTableWidgetItem, QFileDialog
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, qApp, QAction
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MyTable(QTableWidget):
    def __init__(self, r, c):
        super().__init__(r, c)
        self.check_change = True 
        self.init_ui()

    def init_ui(self):
        self.cellChanged.connect(self.c_current)
        self.show()
    
    def c_current(self):
        if self.check_change:            
            self.show()
    
    def open_sheet(self):
        self.check_change = False
        path = QFileDialog.getOpenFileName(self, 'Open CSV', os.getenv('HOME'), 'CSV(*.csv ,  *.xlsx)')
        
        if path[0] != '':
            with open(path[0], newline='') as csv_file:
                self.setRowCount(0)
                self.setColumnCount(7)
                my_file = csv.reader(csv_file, dialect='excel')
                for row_data in my_file:
                    row = self.rowCount()
                    self.insertRow(row)
                    for column, stuff in enumerate(row_data):
                        item = QTableWidgetItem(stuff)
                        self.setItem(row, column, item)
        self.check_change = True   
    
class Sheet(QMainWindow):
    def __init__(self):
        super().__init__()

        self.form_widget = MyTable(14, 7)
        self.setCentralWidget(self.form_widget)
        
        col_headers = ["ID","Connection type","Axial loadC","Shear load","Bolt diameter","Bolt grade","Plate thickness"]
        self.form_widget.setHorizontalHeaderLabels(col_headers)

        b2 = QPushButton('Load Inputs',self)
        b2.move(1500,50)        
        b2.clicked.connect(self.form_widget.open_sheet)
        self.show()
        
app = QApplication(sys.argv)
sheet = Sheet()
sys.exit(app.exec_())