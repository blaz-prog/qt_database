import sys
from PyQt6.QtWidgets import (QApplication, QFormLayout, QWidget,
                             QCompleter, QLineEdit, QLabel, QPushButton)
from PyQt6.QtSql import  QSqlQuery
from PyQt6.QtCore import Qt, QTimer, QModelIndex, pyqtSignal
from PyQt6.QtGui import QStandardItemModel, QStandardItem

class EditCompleter(QLineEdit):
    pk_changed = pyqtSignal(int)
    def __init__(self, parent=None):
        super().__init__(parent)
        # to hold  db_id of record
        self.db_id = None
        self._completer_activated = False
        # define instance attributes
        self.completer = QCompleter()
        self.completer_model = QStandardItemModel()
        self.filter_timer = QTimer()
        self.setup_completer()
        self.textChanged.connect(self.text_changed)
        self.editingFinished.connect(self.editing_finished)

    def setup_completer(self):
        self.completer.setCompletionColumn(0)
        self.completer.setModel(self.completer_model)
        self.completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.completer.setCompletionRole(Qt.ItemDataRole.DisplayRole)
        self.completer.activated[QModelIndex].connect(self.do_complete)
        self.setCompleter(self.completer)
        line_edit = self
        # Connect signals for dynamic filtering
        line_edit.textEdited.connect(self.delayed_filter)
        self.filter_timer.setInterval(300)  # 300ms delay
        self.filter_timer.setSingleShot(True)
        self.filter_timer.timeout.connect(self.filter_items)

    def delayed_filter(self, text):
        """Start timer for filtering (avoids filtering on every keystroke)"""
        self.filter_timer.start()

    def filter_items(self):
        """Query only matching items from database"""
        search_text = self.text()
        self.completer_model.clear()
        self._completer_activated = False
        if len(search_text) < 1:
            return

        num_results = 0
        query = self.get_items(search_text)
        if query.exec():
            while query.next():
                num_results += 1
                item = QStandardItem(query.value(0))
                item.setData(query.value(1), Qt.ItemDataRole.UserRole)
                self.completer_model.appendRow(item)
                # results.append(query.value(0))
            if num_results:
                self.completer.complete()
            else:
                self.completer.popup().hide()

    def get_items(self, filter_text):
        ''''
        Mora vrniti query, ki ima v prvem stolpcu naziv
        v drugem pa database id
        '''
        query = QSqlQuery()
        query.prepare("SELECT naziv, id FROM drzava WHERE naziv ILIKE ? LIMIT 50")
        query.addBindValue(f"{filter_text}%")
        return query


    def text_changed(self, text):
        self._completer_activated = False
        self.set_db_id(None)

    def editing_finished(self):
        # ce sem izbral prek completerja ne iscem se enkrat
        if self._completer_activated:
            return

        entered_text = self.text()
        num_records = 0
        # preverim, ce je venseni text enolicen v bazi
        # Ce obstaja samo en zapis za dolocen vnos potem postavim id
        if self.get_number_of_matches(entered_text) == 1:
            query = QSqlQuery()
            query.prepare("SELECT id, naziv FROM drzava WHERE naziv = ?")
            query.addBindValue(entered_text)
            if query.exec() and query.next():
                self.set_db_id(query.value(0))
            else:
                print(query.lastError().databaseText())
        else:
            self.set_db_id(None)

    def get_number_of_matches(self, filter_text):
        '''
        return number of matches for entered text
        :param filter_text:
        :return:
        '''
        num_records = 0
        query = QSqlQuery()
        query.prepare("SELECT count(*) FROM drzava WHERE naziv = ?")
        query.addBindValue(filter_text)
        if query.exec() and query.next():
            num_records = query.value(0)
        else:
            print(query.lastError().databaseText())

        return num_records

    def set_db_id(self, value):
        self.db_id = value
        self.pk_changed.emit(self.db_id)

    def do_complete(self, model_index):
        """
        Ko izberem prek completerja, si zapomnim database id
        in da je bilo izbrano prek completerja, da ne preverjam dvakrat
        :return:
        """
        item = self.completer_model.item(model_index.row())
        record_id = item.data(Qt.ItemDataRole.UserRole)
        self.set_db_id(record_id)
        self._completer_activated = True

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.le_drzava = EditCompleter()
        self.lbl_drzava_id = QLabel()
        le_ime = QLineEdit()
        layout = QFormLayout()
        layout.addRow("Drzava", self.le_drzava)
        layout.addRow('Drzava id', self.lbl_drzava_id)
        layout.addRow("Ime drzavljana", le_ime)
        self.pb_controla = QPushButton("Kontrola")
        layout.addRow("Kontrola id", self.pb_controla)
        self.pb_controla.clicked.connect(self.do_controla)
        self.le_drzava.pk_changed.connect(self.record_id_changed)
        self.setLayout(layout)

    def do_controla(self):
        self.lbl_drzava_id.setText(str(self.le_drzava.db_id))

    def record_id_changed(self, new_id):
        self.lbl_drzava_id.setText(str(new_id))

if __name__ == '__main__':
    from PyQt6.QtSql import QSqlDatabase
    db = QSqlDatabase.addDatabase("QPSQL")
    db.setUserName('blaz')
    db.setPassword('buratino')
    db.setDatabaseName('kadri')
    if not db.open():
        print("Unable to open database.")
    else:
        print("Database successfully opened.")
    app = QApplication(sys.argv)
    window = MyApp()
    window.resize(400, 100)
    window.show()
    sys.exit(app.exec())
