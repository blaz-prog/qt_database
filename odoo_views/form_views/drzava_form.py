import sys
from PyQt6.QtWidgets import  (QLineEdit,
                              QFormLayout)

from app_models.app_tables import Drzava
from sqlalchemy.orm import Session
from postgresql_engine.engine import engine
from .generic_form import RecordEditForm

class DrzavaForm(RecordEditForm):

    def __init__(self, parent=None, record_id = None):
        super().__init__(parent)
        self.record_list = []
        self.record_id = record_id
        # ustvarim kontrole
        self.le_iso_koda = QLineEdit()
        self.le_naziv = QLineEdit()
        layout_left = QFormLayout()
        layout_left.addRow("Stevilka", self.le_iso_koda)
        layout_left.addRow("Naziv", self.le_naziv)
        self.controls_widget.setLayout(layout_left)
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
                record = session.get(Drzava, record_id)
                self.le_iso_koda.setText(record.iso_koda)
                self.le_naziv.setText(record.naziv)
            self.le_iso_koda.setFocus()
    def prepare_add(self):
        """
        pripravim vnosna polja za vnos novega in napisem
        morebitne privzete vrednosti
        :return:
        """
        self.record_id = None
        self.le_iso_koda.setText("")
        self.le_naziv.setText("")
        self.le_iso_koda.setFocus()

    def save_record(self):
        with Session(engine) as session:
            if self.record_id:
                record = session.get(Drzava, self.record_id)
            else:
                record = Drzava()
            record.iso_koda = self.le_iso_koda.text()
            record.naziv = self.le_naziv.text()
            if not self.record_id:
                session.add(record)
            session.commit()
            session.close()
