import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QApplication,
                             QDialog,
                             QDialogButtonBox,
                             QTableView,
                             QLineEdit,
                             QVBoxLayout,
                             QMessageBox, QSizePolicy, QAbstractItemView)


class LookupDialog(QDialog):
    def __init__(self, parent=None, table_name='table',
                 lookup_class=None, lookup_string=''):
        super().__init__(parent)
        self.selected_id = False
        self.setWindowTitle(f"Lookup {table_name}")
        self.setGeometry(300, 300, 600, 400)
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        self.le_search = QLineEdit()
        self.tv_results = QTableView()
        self.tv_results.setSelectionBehavior(
                QTableView.SelectionBehavior.SelectRows
            )
        self.lookup_string = lookup_string
        self.lookup_class = lookup_class
        if lookup_string:
            lookup_model = lookup_class.name_search(lookup_string)
            self.tv_results.setModel(lookup_model)
        main_layout.addWidget(self.le_search)
        main_layout.addWidget(self.tv_results)
        self.button_box = QDialogButtonBox(
                QDialogButtonBox.StandardButton.Ok |
                QDialogButtonBox.StandardButton.Cancel
        )
        main_layout.addWidget(self.button_box)

        # signals & slots
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.le_search.editingFinished.connect(self.set_new_model)
        self.tv_results.doubleClicked.connect(self.accept)

        # hauskeeping
        self.le_search.setText(self.lookup_string)
        self.tv_results.selectRow(0)
        self.tv_results.resizeColumnsToContents()
        self.tv_results.setFocus()

    def set_new_model(self):
        new_search = self.le_search.text()
        if new_search:
            lookup_model = self.lookup_class.name_search(new_search)
            self.tv_results.setModel(lookup_model)
            self.tv_results.selectRow(0)
            self.tv_results.resizeColumnsToContents()
            self.tv_results.setFocus()

    def accept(self):
        # todo kaksna je razlika med current index in selected index
        index = self.tv_results.selectedIndexes()[0]
        self.selected_id = self.tv_results.model().data(index,
                                        role=Qt.ItemDataRole.DisplayRole)
        self.selected_record = self.lookup_class(self.selected_id)
        super().accept()
