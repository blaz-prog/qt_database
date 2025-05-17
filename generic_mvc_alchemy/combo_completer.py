import sys
from PyQt6.QtWidgets import (QApplication, QComboBox, QWidget,
                             QVBoxLayout, QCompleter, QLineEdit)
from PyQt6.QtSql import QSqlQueryModel, QSqlQuery, QSqlDatabase
from PyQt6.QtCore import Qt, QStringListModel, QTimer, QModelIndex
from PyQt6.QtGui import QStandardItemModel, QStandardItem


class LargeDataComboBox(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_completer()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.combo = QComboBox()
        self.combo.setEditable(True)
        self.combo.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.combo.setCurrentIndex(-1)
        self.layout.addWidget(self.combo)
        self.layout.addWidget(QLineEdit())
        self.layout.addWidget(QLineEdit())
        self.layout.addWidget(QLineEdit())
        self.setWindowTitle('Large Dataset ComboBox')

    def setup_database(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(":memory:")

        if not self.db.open():
            print("Could not open database")
            return

        # Create and populate a large table
        query = QSqlQuery()
        query.exec("CREATE TABLE large_items (id INTEGER PRIMARY KEY, name TEXT)")

        # For demo, insert 100,000 items (in a real app, you'd have existing data)
        query.exec("BEGIN TRANSACTION")
        query.prepare("INSERT INTO large_items (name) VALUES (?)")
        for i in range(1, 101):
            query.addBindValue(f"Item {i}")
            query.exec()
            print('Adding to database')
        query.exec("COMMIT")

    def setup_completer(self):
        # Use a custom completer with delayed filtering
        # self.completer_model = QStringListModel()
        self.completer_model = QStandardItemModel()
        self.completer = QCompleter()
        self.completer.setCompletionColumn(0)
        self.completer.setModel(self.completer_model)
        self.completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.completer.setCompletionRole(Qt.ItemDataRole.DisplayRole)
        self.completer.activated[QModelIndex].connect(self.do_complete)
        self.combo.setCompleter(self.completer)
        line_edit  = self.combo.lineEdit()
        # Connect signals for dynamic filtering
        line_edit.textEdited.connect(self.delayed_filter)
        self.filter_timer = QTimer()
        self.filter_timer.setInterval(300)  # 300ms delay
        self.filter_timer.setSingleShot(True)
        self.filter_timer.timeout.connect(self.filter_items)

    def delayed_filter(self, text):
        """Start timer for filtering (avoids filtering on every keystroke)"""
        self.filter_timer.start()

    def filter_items(self):
        """Query only matching items from database"""
        search_text = self.combo.currentText()
        self.completer_model.clear()
        if len(search_text) < 1:
            return

        query = QSqlQuery()
        query.prepare("SELECT naziv, id FROM drzava WHERE naziv ILIKE ? LIMIT 50")
        query.addBindValue(f"{search_text}%")
        num_results = 0
        if query.exec():
            results = []
            while query.next():
                num_results += 1
                item = QStandardItem(query.value(0))
                item.setData(query.value(1), Qt.ItemDataRole.UserRole)
                self.completer_model.appendRow(item)
                # results.append(query.value(0))
            # Update ONLY the completer model
            # self.completer_model.setStringList(results)

            if num_results:
                self.completer.complete()
            else:
                self.completer.popup().hide()

    def do_complete(self, model_index):
        """
        Ko izberem prek completerja, si zapomnim database id
        :return:
        """
        item = self.completer_model.item(model_index.row())
        record_id = item.data(Qt.ItemDataRole.UserRole)
        print("Selected ID:", item.data(Qt.ItemDataRole.UserRole))
        self.combo.setProperty("record_id", record_id)

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
    window = LargeDataComboBox()
    window.resize(400, 100)
    window.show()
    sys.exit(app.exec())