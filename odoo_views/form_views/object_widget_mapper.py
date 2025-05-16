import sys
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtGui as qtg
from PyQt6 import QtCore as qtc
from PyQt6.QtWidgets import QLineEdit, QComboBox, QCheckBox


class Book:
    def __init__(self, name, author, year_published, sold_out):
        self.name = name
        self.author = author
        self.year_published = year_published
        self.sold_out = sold_out

    def __str__(self):
        return f"{self.name} {self.author} {self.year_published}, {self.sold_out}"

class MainWindow(qtw.QWidget):

    def __init__(self):
        """Main Window constructor"""
        super().__init__()
        self.book = Book("Der dreizehnte Monat", "David Mitchell", 2008, True)
        self.name = qtw.QLineEdit()
        self.name.setProperty('field_name', 'name')
        self.author = qtw.QLineEdit()
        self.author.setProperty('field_name', 'author')
        self.year_published  = qtw.QLineEdit()
        self.year_published.setProperty('field_name', 'year_published')
        self.sold_out = QCheckBox()
        self.sold_out.setProperty('field_name', 'sold_out')

        self.btn_save = qtw.QPushButton("Save")
        self.btn_reread = qtw.QPushButton("Reread")
        form_layout  = qtw.QFormLayout()
        form_layout.addRow("Name", self.name)
        form_layout.addRow("Author", self.author)
        form_layout.addRow("Year published", self.year_published)
        form_layout.addRow("Sold out", self.sold_out)
        form_layout.addRow(self.btn_save, self.btn_reread)
        self.setLayout(form_layout)
        """Main window UI code goes here"""
        self.setWindowTitle('Object Widget Mapper')
        self.map_contorls_to_object(self.book)
        """End Main window UI code"""
        self.show()
        # signals & slots
        self.btn_save.clicked.connect(self.map_object_to_controls)

    def map_contorls_to_object(self, map_object):
        for p in self.book.__dict__:
            print(p)

        for c in self.findChildren((QLineEdit, QComboBox, QCheckBox)):
            db_field = c.property('field_name')
            if db_field:
                val = getattr(self.book, db_field)
                if type(c) == QLineEdit:
                    c.setText(str(val))
                elif type(c) == QCheckBox:
                    c.setChecked(val)


    def map_object_to_controls(self, map_object=None):
        for c in self.findChildren((QLineEdit, QComboBox, QCheckBox)):
            db_field = c.property('field_name')
            val = None
            if db_field:
                if type(c) == QLineEdit:
                    val = c.text()
                elif type(c) == QCheckBox:
                    val = c.isChecked()

                if val:
                    setattr(self.book, db_field, val)


        print(self.book)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mv = MainWindow()
    sys.exit(app.exec())




