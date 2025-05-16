from PyQt6.QtWidgets import QLineEdit, QApplication, QCompleter
from PyQt6.QtSql import QSqlTableModel
from PyQt6 import QtCore


class DBLineEdit(QLineEdit):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_value = None
        self.completer = QCompleter()
        drzave = QSqlTableModel()
        drzave.setTable('drzava')
        drzave.select()
        self.completer.setModel(drzave)
        self.completer.setCompletionColumn(2)
        self.setCompleter(self.completer)
        self.editingFinished.connect(self.dataentry_finished)
        self.completer.activated[QtCore.QModelIndex].connect(self.completer_activated)

    @property
    def db_value(self):
        return self._db_value

    @db_value.setter
    def db_value(self, new_value):
        self._db_value = new_value

    def dataentry_finished(self):
        print(self.text())

    def completer_activated(self, model_index):
        # id je v 0-ti koloni
        completer_model = model_index.model()
        ind0 = completer_model.index(model_index.row(), 0)
        self.db_value = ind0.data()
        print("Completer activated", self.db_value)


