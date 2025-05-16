from PyQt6.QtWidgets import QLineEdit, QApplication, QCompleter
from PyQt6 import QtCore



class DBLineEdit(QLineEdit):

    def __init__(self, model, completer,  parent=None):
        super().__init__(parent)
        self._db_value = None
        self.model = model()
        self.completer = completer()
        self.setCompleter(self.completer)
        self.editingFinished.connect(self.dataentry_finished)

        self.completer.activated[QtCore.QModelIndex].connect(self.completer_activated)

    @property
    def db_value(self):
        return self._db_value

    @db_value.setter
    def db_value(self, new_value):
        if new_value:
            self._db_value = new_value
            self.setText(self.model.get_by_id(self._db_value))
        else:
            self._db_value=False
            self.setText("")

    def dataentry_finished(self):
        search_results = self.model.query_data(self.text(), exact=True)
        if len(search_results)  == 1:
            rec = search_results[0]
            self.db_value = rec.id_get()
            self.setText(rec.name_get())
        elif len(search_results) > 1:
            self.completer.complete()

    def completer_activated(self, model_index):
        completer_model = model_index.model()
        ind0 = completer_model.index(model_index.row(), 0)

        print(ind0.data())
