import sys
from PyQt6.QtWidgets import (QWidget, QTableView, QVBoxLayout, QHBoxLayout,
                             QGroupBox, QLineEdit,QLabel, QTextEdit, QDialog, QComboBox,
                             QFormLayout, QGridLayout, QPushButton, QApplication, QHeaderView,
                             QDialogButtonBox, QMessageBox)
from sqlalchemy import select
from app_models.app_tables import Delojemalec
from postgresql_engine.engine import  engine, session
from generic_mvc_alchemy.generic_table_model import GenericTableModel
from generic_mvc_alchemy.generic_table_browser import GenericTableBrowser
import datetime

class DelojemalecModel(GenericTableModel):
    FIELDS_HEADERS = [
        ('ime', 'Ime'),
        ('priimek', 'Priimek'),
        ('davcna_stevilka', "Davčna številka"),
        ('ulica', "Ulica/Kraj"),
        ('posta', "Posta"),
        ('spol', "Spol")
    ]
    def __init__(self):
        super().__init__(session)

    def query_data(self, search_filter):
        stmt = select(Delojemalec)
        if search_filter:
            stmt = stmt.where(
                (Delojemalec.priimek.ilike(f"{search_filter}%"))
            )
        return session.scalars(stmt).all()


class DelojemalecBrowser(GenericTableBrowser):
    pass


class DelojemalecForm(QDialog):
    def __init__(self, parent=None, record=None):
        super().__init__(parent)
        self.record = record
        # ustvarim kontrole
        self.le_ime = QLineEdit()
        self.le_priimek = QLineEdit()
        self.le_ulica = QLineEdit()
        self.le_posta = QLineEdit()
        self.le_drzava = QLineEdit()
        self.le_datum_rojstva = QLineEdit()
        self.le_davcna_stevilka = QLineEdit()
        self.le_emso = QLineEdit()
        self.le_spol = QComboBox()
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok |
                                           QDialogButtonBox.StandardButton.Cancel)

        if self.record:
            self.setWindowTitle('Urejanje delojemalca')
            self.le_ime.setText(self.record.ime)
            self.le_priimek.setText(self.record.priimek)
            self.le_ulica.setText(self.record.ulica)
            self.le_davcna_stevilka.setText(self.record.davcna_stevilka)
            self.le_posta.setText('500')
            self.le_drzava.setText(self.record.drzava)
            self.le_datum_rojstva.setText(datetime.datetime.strftime(record.datum_rojstva, '%Y-%m-%d'))
            self.le_emso.setText(self.record.emso)
            self.le_davcna_stevilka.setText(self.record.davcna_stevilka)
            self.record.spol = "M"

        else:
            self.setWindowTitle('Dodajanje delojemalca')

        edit_layout = QHBoxLayout()
        layout_left = QFormLayout()
        layout_left.addRow("Ime", self.le_ime)
        layout_left.addRow("Priimek", self.le_priimek)
        layout_left.addRow("Ulica", self.le_ulica)
        layout_left.addRow("Posta", self.le_posta)
        layout_left.addRow("Drzava", self.le_drzava)
        layout_left.addRow(self.button_box)
        layout_right = QFormLayout()
        layout_right.addRow("Datum rojstva", self.le_datum_rojstva)
        layout_right.addRow("Davčna številka", self.le_davcna_stevilka)
        layout_right.addRow("Emšo", self.le_emso)
        layout_right.addRow("Spol", self.le_spol)
        edit_layout.addLayout(layout_left)
        edit_layout.addLayout(layout_right)
        main_layout = QVBoxLayout()
        main_layout.addLayout(edit_layout)
        main_layout.addWidget(self.button_box)
        self.setLayout(main_layout)
        # signals & slots
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        # housekeeping
        self.resize(768, 363)

    def accept(self):
        # Potrdil sem formo, shranim zapis
        if not self.record:
            self.record = Delojemalec()
        self.record.ime = self.le_ime.text()
        self.record.priimek = self.le_priimek.text()
        self.record.ulica = self.le_ulica.text()
        self.record.davcna_stevilka = self.le_davcna_stevilka.text()
        self.record.posta = 500
        self.record.drzava = self.le_drzava.text()
        self.record.datum_rojstva = self.le_datum_rojstva.text()
        self.record.emso = self.le_emso.text()
        self.record.davcna_stevilka = self.le_davcna_stevilka.text()
        self.record.spol = "M"
        super().accept()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = DelojemalecBrowser(
        table_model = DelojemalecModel,
        edit_form = DelojemalecForm)
    mw.setWindowTitle('Delojemalci')
    mw.show()
    sys.exit(app.exec())
