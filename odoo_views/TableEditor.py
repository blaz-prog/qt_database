import sys
from PyQt6.QtWidgets import (QWidget, QTableView, QVBoxLayout, QHBoxLayout,
                             QGroupBox, QLineEdit,
                             QPushButton, QApplication, QHeaderView,
                             QMessageBox, QStackedWidget, QLabel)
from PyQt6.QtCore import Qt, QEvent, QSortFilterProxyModel, QSettings, QRect
from PyQt6.QtGui import QIcon
from delojemalec import DelojemalecModel
from posta import PostaModel
from form_views.delojemalec_form import DelojemalecForm
from form_views.poste_form import PostaForm
from common import resources
class TableEditor(QWidget):

    def __init__(self, table_model, form_widget, parent=None, load=True):
        super().__init__(parent)
        self.stack_widget = QStackedWidget()
        self.table_view = QTableView()
        self.model = table_model()
        self.icon_form_view = QIcon(":/icons/form-view.png")
        self.icon_table_view = QIcon(":/icons/table-view.png")
        if load:
            self.model.load()
        self.form = form_widget(parent=self)
        # orodna vrstica
        main_layout = QVBoxLayout()
        toolbar_widget = QWidget()
        toolbar_widget.setStyleSheet("""
            background-color: #817a78;
        """)
        toolbar_layout  = QHBoxLayout()
        self.btn_new = QPushButton("Nov")
        self.btn_new.setIcon(QIcon(":/icons/add-record.png"))
        self.lbl_title = QLabel(self.model.TITLE)
        self.le_search = QLineEdit()
        self.le_search.setPlaceholderText('Iskanje...')
        self.lbl_rec_no = QLabel()

        icon_previous = QIcon(":/icons/arrow-180.png")
        self.btn_previous = QPushButton()
        self.btn_previous.setIcon(icon_previous)
        icon_next = QIcon(":/icons/arrow.png")
        self.btn_next = QPushButton()
        self.btn_next.setIcon(icon_next)

        self.btn_toggle = QPushButton()
        self.btn_toggle.setIcon(self.icon_form_view)

        toolbar_layout.addWidget(self.btn_new)
        toolbar_layout.addWidget(self.lbl_title)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.le_search)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.lbl_rec_no)
        toolbar_layout.addWidget(self.btn_previous)
        toolbar_layout.addWidget(self.btn_next)
        toolbar_layout.addWidget(self.btn_toggle)
        toolbar_widget.setLayout(toolbar_layout)
        # main_layout.addLayout(toolbar_layout)
        main_layout.addWidget(toolbar_widget)
        # tabelaricni pregled
        self.table_view = QTableView()
        self.table_view.installEventFilter(self)
        self.table_view.setModel(self.model)
        self.table_view.resizeColumnsToContents()
        self.set_columns_width()
        main_layout.addWidget(self.stack_widget)
        self.stack_widget.addWidget(self.table_view)
        self.stack_widget.addWidget(self.form)
        self.setLayout(main_layout)

        # signals and slots
        self.le_search.editingFinished.connect(self.reload_model)
        self.table_view.doubleClicked.connect(self.show_edit_form)
        self.btn_new.clicked.connect(self.add_record)
        self.btn_toggle.clicked.connect(self.toggle_view)
        self.stack_widget.currentChanged.connect(self.view_changed)
        self.btn_next.clicked.connect(self.move_to_next_record)
        self.btn_previous.clicked.connect(self.move_to_previous_record)

        # hauskeeping
        self.table_view.setFocus()
        self.table_view.selectRow(0)
        self.read_settings()

    def eventFilter(self, obj, event):
        if obj == self.table_view:
            if event.type() == QEvent.Type.KeyPress:
                if event.key() == Qt.Key.Key_Return:
                    self.show_edit_form()
        return super().eventFilter(obj, event)

    # slots definition

    def reload_model(self):
        self.stack_widget.setCurrentWidget(self.table_view)
        self.model.load(self.le_search.text())
        self.table_view.resizeRowsToContents()
        self.set_columns_width()
        self.table_view.setFocus()
        self.table_view.selectRow(0)
        self.set_columns_width()

    def show_edit_form(self):
        current_index = self.table_view.currentIndex()
        record = self.model.record_list[current_index.row()]
        self.stack_widget.setCurrentWidget(self.form)
        self.form.read_record(record.id)

    def add_record(self):
        self.stack_widget.setCurrentWidget(self.form)
        self.form.prepare_add()

    def toggle_view(self):
        if self.stack_widget.currentWidget() == self.table_view:
            self.show_edit_form()
        elif self.stack_widget.currentWidget() == self.form:
            self.stack_widget.setCurrentWidget(self.table_view)

    def view_changed(self, index):
        """
        :param index: že spremenjeni index
        :return:
        """
        if index == self.stack_widget.indexOf(self.table_view):
            self.model.load(self.le_search.text())
            self.table_view.resizeRowsToContents()
            self.set_columns_width()
            self.btn_toggle.setIcon(self.icon_form_view)
        elif index == self.stack_widget.indexOf(self.form):
            self.btn_toggle.setIcon(self.icon_table_view)

    def move_to_next_record(self):
        current_index = self.table_view.currentIndex().row()
        current_index += 1
        if current_index < len(self.table_view.model().record_list):
            record = self.model.record_list[current_index]
            self.table_view.selectRow(current_index)
            if self.stack_widget.currentWidget() == self.form:
                self.form.read_record(record.id)

    def move_to_previous_record(self):
        current_index = self.table_view.currentIndex().row()
        if current_index > 0:
            current_index -=1
            record = self.model.record_list[current_index]
            self.table_view.selectRow(current_index)
            if self.stack_widget.currentWidget() == self.form:
                self.form.read_record(record.id)



    def closeEvent(self, event):
        self.save_settings()
        event.accept()

    def save_settings(self):
        settings = QSettings()
        settings.setValue("geometryTableBrowser", self.geometry())
        column_widths = []
        for col in range(0, self.table_view.model().columnCount()):
            print(self.table_view.columnWidth(col))
            column_widths.append(self.table_view.columnWidth(col))
        print(self.table_view.objectName())
        settings.setValue("column_widths", column_widths)

    @staticmethod
    def read_settings():
        settings = QSettings()
        init_geometry = settings.value("geometryTableBrowser", QRect(200, 200, 1000, 800))
        return init_geometry

    def set_columns_width(self):
        settings = QSettings()
        column_widths = settings.value("column_widths", False)
        if column_widths:
            for col, w in enumerate(column_widths):
                self.table_view.setColumnWidth(col, int(w))
        else:
            self.table_view.resizeColumnsToContents()

if __name__ == '__main__':
    import os
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
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.

    mw = TableEditor(DelojemalecModel, DelojemalecForm)
    mw.setWindowTitle('Delojemalci')

    # mw = TableEditor(PostaModel, PostaForm)
    # mw.setWindowTitle('Delojemalci')

    mw.show()
    sys.exit(app.exec())
