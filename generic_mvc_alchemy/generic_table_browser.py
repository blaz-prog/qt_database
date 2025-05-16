from PyQt6.QtWidgets import (QWidget, QTableView, QVBoxLayout, QHBoxLayout,
                             QGroupBox, QLineEdit,
                             QPushButton, QApplication, QHeaderView,
                             QMessageBox)

from PyQt6.QtCore import Qt, QEvent, QSortFilterProxyModel, QSettings, QRect


class GenericTableBrowser(QWidget):
    """
    Kot model uporabljam QSqlTableModel
    """
    def __init__(self, table_model, edit_form=None):
        super().__init__()
        self.engine = QApplication.property(self, 'engine')
        self.edit_form = edit_form
        # Main UI code goes here
        self.setWindowTitle("Generic Browser")
        # get model
        self.model = table_model()
        self.model.load()
        # setup view
        grupbox = QGroupBox('Search')
        self.le_search = QLineEdit()
        grupbox_layout = QHBoxLayout()
        grupbox_layout.addWidget(self.le_search)
        grupbox.setLayout(grupbox_layout)
        # tabela, ki bo kazala zapise
        self.table_view = QTableView()
        self.table_view.installEventFilter(self)
        self.table_view.setModel(self.model)
        self.table_view.resizeColumnsToContents()
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.horizontalHeader().setSectionResizeMode(len(self.table_view.model().FIELDS_HEADERS)-1,
                                                                QHeaderView.ResizeMode.Stretch)
        # razporedim vse na formo
        main_layout = QVBoxLayout()
        main_layout.addWidget(grupbox)
        table_layout = QHBoxLayout()
        table_layout.addWidget(self.table_view)
        table_buttons_sublayout = QVBoxLayout()
        self.btn_add = QPushButton("Add")
        self.btn_delete = QPushButton("Delete")
        table_buttons_sublayout.addWidget(self.btn_add)
        table_buttons_sublayout.addWidget(self.btn_delete)
        table_buttons_sublayout.addStretch()
        table_layout.addLayout(table_buttons_sublayout)
        main_layout.addLayout(table_layout)

        self.setLayout(main_layout)
        # End main UI code

        # signals, slots and events
        self.le_search.editingFinished.connect(self.reload_model)
        self.table_view.doubleClicked.connect(self.show_edit_form)
        self.btn_add.clicked.connect(self.add_record)
        self.btn_delete.clicked.connect(self.delete_record)
        # houskeeping
        if not self.edit_form:
            self.btn_add.setDisabled(True)
            self.btn_delete.setDisabled(True)
        # hauskeeping
        self.read_settings()

    def eventFilter(self, obj, event):
        if obj == self.table_view:
            if event.type() == QEvent.Type.KeyPress:
                if event.key() == Qt.Key.Key_Return:
                    self.show_edit_form()
        return super().eventFilter(obj, event)

    def show_edit_form(self):
        current_index = self.table_view.currentIndex()
        record = self.model.record_list[current_index.row()]
        form = self.edit_form(self, record)
        if form.exec():
            self.model.db_session.commit()
            self.model.dataChanged.emit(current_index, current_index)

    def delete_record(self):
        current_index = self.table_view.currentIndex()
        if not current_index:
            return

        button =QMessageBox.question(self, "Confirm delete",
                                     "Please, confirm record delition")
        if button == QMessageBox.StandardButton.Yes:
            self.model.delete_record(current_index.row())

    def add_record(self):
        form = self.edit_form(self)
        if form.exec():
            self.model.add(form.record)

    def reload_model(self):
        new_filter = self.le_search.text()
        self.model.load(new_filter)
        self.table_view.resizeRowsToContents()

    def closeEvent(self, event):
        self.save_settings()
        event.accept()

    def save_settings(self):
        settings = QSettings()
        settings.setValue("geometryTableBrowser", self.geometry())

    def read_settings(self):
        settings = QSettings()
        init_geometry = settings.value("geometryTableBrowser", QRect(200, 200, 400, 600)).toRect()
        self.setGeometry(init_geometry)
