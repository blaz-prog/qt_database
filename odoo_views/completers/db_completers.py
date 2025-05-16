from PyQt6.QtWidgets import QCompleter
from PyQt6.QtSql import QSqlTableModel, QSqlQueryModel

class PosteCompleter(QCompleter):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = QSqlTableModel()
        self.model.setTable('posta')
        self.model.select()
        self.setModel(self.model)
        self.setCompletionColumn(2)

class DrzaveCompleter(QCompleter):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = QSqlTableModel()
        self.model.setTable('drzava')
        self.model.select()
        self.setModel(self.model)
        self.setCompletionColumn(2)

class PogodbaCompleter(QCompleter):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = QSqlTableModel()
        self.model.setTable('pogodba')
        self.model.select()
        self.setModel(self.model)
        self.setCompletionColumn(2)

class DelojemalecCompleter(QCompleter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = QSqlTableModel()
        self.model.setTable('delojemalec')
        self.model.select()
        self.setModel(self.model)
        self.setCompletionColumn(2)


class KategorijaIzplacilaCompleter(QCompleter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = QSqlTableModel()
        self.model.setTable('kategorija_izplacila')
        self.model.select()
        self.setModel(self.model)
        self.setCompletionColumn(2)

class VrstaIzplacilaCompleter(QCompleter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = QSqlTableModel()
        self.model.setTable('vrsta_izplacila')
        self.model.select()
        self.setModel(self.model)
        self.setCompletionColumn(2)
