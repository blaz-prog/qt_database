import sys
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QIcon, QKeySequence
from PyQt6.QtWidgets import (QApplication,
                             QWidget,
                             QDialogButtonBox,
                             QTableView,
                             QLineEdit,
                             QPushButton,
                             QVBoxLayout, QFormLayout,
                             QHBoxLayout,
                             QStackedWidget,
                             QTableView,
                             QDataWidgetMapper,
                             QMessageBox, QSizePolicy, QAbstractItemView, QHeaderView)

from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlTableModel
import db

WINDOW_TITLE = 'Urejanje držav'
WINDOW_GEOMETRY = (300, 300, 500, 350)
class DrzavaForm(QWidget):

    FIRST, PREV, NEXT, LAST = range(4)
    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(*WINDOW_GEOMETRY)

        main_layout = QVBoxLayout()
        form_layout = QFormLayout()
        self.iso_koda = QLineEdit()
        self.naziv = QLineEdit()
        form_layout.addRow('Iso koda', self.iso_koda)
        form_layout.addRow('Naziv', self.naziv)
        button_layout = QHBoxLayout()
        btn_first = QPushButton("<<")
        btn_last = QPushButton(">>")
        btn_next = QPushButton(">")
        btn_previous = QPushButton("<")
        btn_add = QPushButton("Dodaj")
        button_layout.addWidget(btn_add)
        button_layout.addStretch()
        button_layout.addWidget(btn_first)
        button_layout.addWidget(btn_previous)
        button_layout.addWidget(btn_next)
        button_layout.addWidget(btn_last)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(form_layout)
        self.setLayout(main_layout)

        # connecting to database
        self.model = QSqlTableModel(self)
        self.model.setTable('drzava')
        self.model.setSort(1, Qt.SortOrder.AscendingOrder)
        self.model.select()
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.SubmitPolicy.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.iso_koda, 1)
        self.mapper.addMapping(self.naziv, 2)
        self.mapper.toFirst()
        btn_first.clicked.connect(lambda: self.save_record(DrzavaForm.FIRST))
        btn_last.clicked.connect(lambda: self.save_record(DrzavaForm.LAST))
        btn_previous.clicked.connect(lambda: self.save_record(DrzavaForm.PREV))
        btn_next.clicked.connect(lambda: self.save_record(DrzavaForm.NEXT))
        btn_next.setShortcut(QKeySequence("Ctrl+N"))
        btn_add.clicked.connect(self.add_record)

    def save_record(self, where):
        row = self.mapper.currentIndex()
        self.mapper.submit()
        if where == DrzavaForm.FIRST:
            row = 0
        elif where == DrzavaForm.PREV:
            row = 0 if row <= 1 else row - 1
        elif where == DrzavaForm.NEXT:
            row += 1
        if row >= self.model.rowCount():
            row = self.model.rowCount() - 1
        elif where == DrzavaForm.LAST:
            row = self.model.rowCount() - 1

        self.mapper.setCurrentIndex(row)

    def add_record(self):
        row = self.model.rowCount()
        self.mapper.submit()
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)
        self.iso_koda.setFocus()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    drzave = DrzavaForm()
    drzave.show()
    sys.exit(app.exec())
