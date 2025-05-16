import sys
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtGui as qtg
from PyQt6 import QtCore as qtc
from PyQt6.QtWidgets import QPushButton

from sqlalchemy.orm import Session

from generic_mvc_alchemy.generic_lookup import DBLineEdit
from odoo_views.delojemalec import DelojemalecModel
from odoo_views.completers.db_completers import DelojemalecCompleter
from app_models.app_tables import Delojemalec, Otrok
from postgresql_engine.engine import engine
from alchemy_model import AlchemyTableModel

class OtrociForm(qtw.QWidget):

    def __init__(self, delojemalec_id=None,  parent=None):
        """Main Window constructor"""
        super().__init__()

        self.form_session = Session(engine)
        self.delojemalec_id = delojemalec_id
        if delojemalec_id:
            self.delojemalec = self.form_session.get(Delojemalec, delojemalec_id)
        else:
            self.delojemalec = Delojemalec()
        self.model_otroci = AlchemyTableModel(self.form_session, self.delojemalec)
        """Main window UI code goes here"""
        main_layout = qtw.QVBoxLayout()
        master_layout = qtw.QFormLayout()
        detail_layout = qtw.QVBoxLayout()
        main_layout.addLayout(master_layout)
        main_layout.addLayout(detail_layout)

        self.le_delojemalec_id = DBLineEdit(DelojemalecModel, DelojemalecCompleter)
        btn_save = QPushButton("Save")
        btn_save.clicked.connect(self.save_record)
        master_layout.addRow(btn_save)
        master_layout.addRow("Delojemalec", self.le_delojemalec_id)
        self.tw_otroci = qtw.QTableView()
        self.tw_otroci.setModel(self.model_otroci)
        btn_add_row = QPushButton("Add")
        btn_delete_row = QPushButton("Delete")
        table_controls = qtw.QHBoxLayout()
        table_controls.addWidget(btn_add_row)
        table_controls.addWidget(btn_delete_row)
        table_controls.addStretch()
        btn_add_row.clicked.connect(self.add_row)
        detail_layout.addLayout(table_controls)
        detail_layout.addWidget(self.tw_otroci)
        self.setLayout(main_layout)
        self.setWindowTitle('Otroci Zaposlenih')

        self.le_delojemalec_id.editingFinished.connect(self.fill_controls)

        self.show()

    def add_row(self):
        print("Dodajam otroka")
        self.delojemalec.otroci.append(Otrok(ime="Mojca", starost=2))
        self.model_otroci.layoutChanged.emit()

    def save_record(self):
        self.form_session.commit()

    def fill_controls(self):
        if self.le_delojemalec_id.db_value:
            self.delojemalec_id = self.le_delojemalec_id.db_value
            self.delojemalec = self.form_session.get(Delojemalec, self.delojemalec_id)
        else:
            self.delojemalec = Delojemalec()
        self.model_otroci = AlchemyTableModel(self.form_session, self.delojemalec)
        self.tw_otroci.setModel(self.model_otroci)

    def closeEvent(self, event):
        print("Closing widget")
        self.form_session.close()
        event.accept()


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
    app = qtw.QApplication(sys.argv)
    mv = OtrociForm()
    sys.exit(app.exec())
