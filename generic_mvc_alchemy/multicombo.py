import sys
from PyQt6.QtWidgets import (QApplication, QWidget,
                             QPushButton, QComboBox,
                             QHBoxLayout, QVBoxLayout)

from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QStandardItem


class CheckableComboBox(QComboBox):

    def __init__(self):
        super().__init__()
        self.setEditable(True)
        self.lineEdit().setReadOnly(False)
        self.closeOnLineEditClick = False
        self.lineEdit().installEventFilter(self)
        self.lineEdit().textChanged.connect(self.on_edit)
        self.view().viewport().installEventFilter(self)
        print(type(self.view().viewport().children()))
        self.model().dataChanged.connect(self.updateLineEditField)

    def on_edit(self, text):
        print(text)
        if len(text) == 0:
            self.hidePopup()
            self.closeOnLineEditClick = False
        else:
            self.showPopup()
            self.lineEdit().setFocus()
            self.closeOnLineEditClick = True

    def eventFilter(self, widget, event):
        if widget == self.lineEdit():
            if event.type() == QEvent.Type.MouseButtonRelease:
                if self.closeOnLineEditClick:
                    self.hidePopup()  # TODO
                else:
                    self.showPopup()
                return True
            elif event.type() == QEvent.Type.KeyRelease:
                print("key release")
                return True
            return super().eventFilter(widget, event)

        if widget == self.view().viewport():
            if event.type == QEvent.Type.MouseButtonRelease:
                indx = self.view().indexAt(event.pos)
                item = self.model().item(indx.row())

                if item.checkState == Qt.CheckState.Checked:
                    item.setCheckState(Qt.CheckState.Unchecked)
                else:
                    item.setCheckState(Qt.CheckState.Checked)
                return True
            elif event.type() == QEvent.Type.KeyRelease:
                print("key release")
                return True
            return super().eventFilter(widget, event)

    def addItems(self, items, itemList=None):
        for index, text in enumerate(items):
            try:
                data = itemList[index]
            except(TypeError, IndexError):
                data= None
            self.addItem(text, data)
        self.lineEdit().setText('')

    def addItem(self, text, userData=None):
        item = QStandardItem()
        item.setText(text)
        if not userData is None:
            item.setData(userData)

        # enable checkbox settings
        item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable)
        item.setData(Qt.CheckState.Unchecked, Qt.ItemDataRole.CheckStateRole)
        self.model().appendRow(item)

    def updateLineEditField(self):
        text_container = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.CheckState.Checked:
                text_container.append(self.model().item(i).text())
        text_string = ", ".join(text_container)
        self.lineEdit().setText(text_string)

    def hidePopup(self):
        super().hidePopup()
        self.startTimer(100)


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.window_width , self.window_height = 1200, 400
        self.setMinimumSize(self.window_width, self.window_height)
        self.setStyleSheet('''
            QWidget {
                font-size: 15px;
            }
        ''')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        combobox = CheckableComboBox()
        combobox.addItems(colors)
        self.layout.addWidget(combobox)
        btn = QPushButton('Retrive', clicked=lambda: print(combobox.currentText()))
        self.layout.addWidget(btn)
        self.cbo_test = QComboBox()
        self.cbo_test.addItem('Master')
        self.cbo_test.addItem('Margarita')
        self.cbo_test.addItem('Voland')
        self.cbo_test.addItem('Begemot')
        self.cbo_test.addItem('Azazel')
        self.cbo_test.addItem('Fagot')
        self.cbo_test.setEditable(True)
        self.cbo_test.lineEdit().setText("")
        self.layout.addWidget(self.cbo_test)

        self.layout.addStretch()


if __name__ == "__main__":
    colors = ['Blue', 'Yellow', 'Orange', 'Green', 'Teal', 'Blue', 'Pink', 'Black', 'White']
    app = QApplication(sys.argv)
    myApp = MyApp()
    myApp.show()
    try:
        sys.exit(app.exec())
    except SystemExit:
        print("Error executing app")

