import sys
from PyQt6.QtWidgets import  (QLineEdit, QTextEdit,
                              QFormLayout)

from app_models.app_tables import VrstaIzplacila
from sqlalchemy.orm import Session
from postgresql_engine.engine import engine
from .generic_form import RecordEditForm
from generic_mvc_alchemy.generic_lookup import DBLineEdit
from odoo_views.completers.db_completers import KategorijaIzplacilaCompleter
from odoo_views.kategorija_izplacila import KategorijaIzplacilaModel

class VrstaIzplacilaForm(RecordEditForm):

    def __init__(self, parent=None, record_id = None):
        super().__init__(parent)
        self.record_list = []
        self.record_id = record_id
        # ustvarim kontrole
        self.le_oznaka = QLineEdit()
        self.le_naziv = QLineEdit()
        self.le_kategorija = DBLineEdit(KategorijaIzplacilaModel, KategorijaIzplacilaCompleter)
        self.le_formula = QTextEdit()
        controls_layout = QFormLayout()
        controls_layout.addRow("Oznaka", self.le_oznaka)
        controls_layout.addRow("Naziv", self.le_naziv)
        controls_layout.addRow("Kategorija", self.le_kategorija )
        controls_layout.addRow("Formula", self.le_formula)
        self.controls_widget.setLayout(controls_layout)
        # housekeeping

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
                record = session.get(VrstaIzplacila, record_id)
                self.le_oznaka.setText(record.oznaka)
                self.le_naziv.setText(record.naziv)
                self.le_formula.setText(record.formula)
                self.le_kategorija.db_value = record.kategorija_id
                # self.le_drzava.setText(record.drzava)

    def prepare_add(self):
        self.record_id = None
        self.le_oznaka.setText("")
        self.le_naziv.setText("")
        self.le_formula.setText("")
        self.le_kategorija.db_value = False

    def save_record(self):
        with Session(engine) as session:
            if self.record_id:
                record = session.get(VrstaIzplacila, self.record_id)
            else:
                record = VrstaIzplacila()
            record.oznaka = self.le_oznaka.text()
            record.naziv = self.le_naziv.text()
            record.kategorija_id = self.le_kategorija.db_value
            record.formula = self.le_formula.toPlainText()
            if not self.record_id:
                session.add(record)
            session.commit()
            session.close()
