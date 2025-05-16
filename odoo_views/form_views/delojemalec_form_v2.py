import sys
from PyQt6.QtWidgets import (QWidget, QTableView, QVBoxLayout, QHBoxLayout,
                             QGroupBox, QLineEdit,QLabel, QTextEdit, QDialog, QComboBox,
                             QFormLayout, QGridLayout, QPushButton, QApplication, QHeaderView,
                             QDialogButtonBox, QMessageBox)


from app_models.app_tables import Delojemalec
from .generic_form import RecordEditForm
from datetime import datetime
from sqlalchemy.orm import Session
from postgresql_engine.engine import engine
from generic_mvc_alchemy.generic_lookup import DBLineEdit

class DelojemalecForm(RecordEditForm):

    def __init__(self, parent=None, record_id = None):
        super().__init__(parent)
        self.record_list = []
        self.record_id = record_id
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
        edit_layout = QHBoxLayout()
        layout_left = QFormLayout()
        layout_left.addRow("Ime", self.le_ime)
        layout_left.addRow("Priimek", self.le_priimek)
        layout_left.addRow("Ulica", self.le_ulica)
        layout_left.addRow("Posta", self.le_posta)
        layout_left.addRow("Drzava", self.le_drzava)
        layout_right = QFormLayout()
        layout_right.addRow("Datum rojstva", self.le_datum_rojstva)
        layout_right.addRow("Davčna številka", self.le_davcna_stevilka)
        layout_right.addRow("Emšo", self.le_emso)
        layout_right.addRow("Spol", self.le_spol)
        edit_layout.addLayout(layout_left)
        edit_layout.addLayout(layout_right)
        main_controls_layout = QHBoxLayout()
        main_controls_layout.addLayout(edit_layout)
        self.controls_widget.setLayout(main_controls_layout)

    def read_record(self, record_id):
        """
        Read record from database and show on form
        :param record_id:
        :return:
        """
        if record_id:
            self.record_id = record_id
            self.setWindowTitle('Urejanje delojemalca')
            with Session(engine) as session:
                record = session.get(Delojemalec, record_id)
                self.le_ime.setText(record.ime)
                self.le_priimek.setText(record.priimek)
                self.le_ulica.setText(record.ulica)
                self.le_davcna_stevilka.setText(record.davcna_stevilka)
                self.le_posta.setText('500')
                self.le_drzava.setText(record.drzava)
                self.le_datum_rojstva.setText(datetime.strftime(record.datum_rojstva, '%Y-%m-%d'))
                self.le_emso.setText(record.emso)
                self.le_davcna_stevilka.setText(record.davcna_stevilka)

    def prepare_add(self):
        self.record_id = None
        self.le_ime.setText("")
        self.le_priimek.setText("")
        self.le_ulica.setText("")
        self.le_davcna_stevilka.setText("")
        self.le_posta.setText('500')
        self.le_drzava.setText("")
        self.le_datum_rojstva.setText("")
        self.le_emso.setText("")
        self.le_davcna_stevilka.setText("")

    def save_record(self):
            with Session(engine) as session:
                if self.record_id:
                    record = session.get(Delojemalec, self.record_id)
                else:
                    record = Delojemalec()
                record.ime = self.le_ime.text()
                record.priimek = self.le_priimek.text()
                record.ulica = self.le_ulica.text()
                record.davcna_stevilka = self.le_davcna_stevilka.text()
                record.posta = self.le_posta.text()
                record.drzava = self.le_drzava.text()
                record.datum_rojstva = self.le_datum_rojstva.text()
                record.emso = self.le_emso.text()
                record.davcna_stevilka = self.le_davcna_stevilka.text()
                record.spol = "M"
                if not self.record_id:
                    session.add(record)
                session.commit()
                session.close()
