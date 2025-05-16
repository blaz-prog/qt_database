import sys
from PyQt6.QtWidgets import (QApplication, QWidget,
                             QPushButton, QComboBox,
                             QLineEdit,
                             QHBoxLayout, QVBoxLayout, QDialog, QListWidget)

from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QStandardItem

class EntryHelp(QListWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.hide()


class DialogTest(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Testing dialog')
        self.setGeometry(20, 20, 800, 600)
        self.le_edit = QLineEdit()
        self.cbo = QComboBox()
        self.cbo.setEditable(True)
        self.le2 = QLineEdit()
        self.entry_help = EntryHelp(self)
        layout = QVBoxLayout()
        layout.addWidget(self.le_edit)
        layout.addWidget(self.cbo)
        layout.addWidget(self.le2)
        layout.addStretch()
        self.setLayout(layout)
        self.le_edit.textEdited.connect(self.show_help)
        self.le_edit.editingFinished.connect(self.hide_help)

    def show_help(self):
        self.entry_help.setGeometry(self.le_edit.geometry())
        self.entry_help.move(self.le_edit.x(), self.le_edit.y() + 30)
        self.entry_help.setFixedHeight(200)
        self.entry_help.raise_()
        self.entry_help.show()

    def hide_help(self):
        self.entry_help.hide()


if __name__ == "__main__":
    colors = ['Blue', 'Yellow', 'Orange', 'Green', 'Teal', 'Blue', 'Pink', 'Black', 'White']
    app = QApplication(sys.argv)
    myApp = DialogTest()
    myApp.show()
    try:
        sys.exit(app.exec())
    except SystemExit:
        print("Error executing app")

