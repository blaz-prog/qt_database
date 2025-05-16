from PyQt6.QtWidgets import QLineEdit, QListWidget, QWidget, QVBoxLayout, QCompleter



class DbPicker(QLineEdit):

    def __init__(self,list_widget,  parent=None):
        super().__init__(parent)
        self.parent = parent
        self.list = list_widget
        self.list.hide()
        self.textEdited.connect(self.on_edit)
        self.editingFinished.connect(self.on_finish)

    def on_edit(self, text):
        if len(text) > 0:
            if not self.list.isVisible():
                self.list.setGeometry(self.geometry())
                self.list.setStyleSheet("background-color:red")
                self.list.setFixedHeight(400)
                self.list.move(self.x(), self.y() + self.height() + 10)
                self.list.show()
        else:
            self.list.hide()


    def on_finish(self):
        self.list.hide()






