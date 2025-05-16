import sys
from PyQt6.QtWidgets import  (QLineEdit,
                             QFormLayout)

from app_models.app_tables import Posta
from sqlalchemy.orm import Session
from postgresql_engine.engine import engine
from .generic_form import RecordEditForm

class PostaForm(RecordEditForm):

    def __init__(self, parent=None, record_id = None):
        super().__init__(parent)
        self.record_list = []
        self.record_id = record_id
        # ustvarim kontrole
        self.le_stevilka = QLineEdit()
        self.le_naziv = QLineEdit()
        self.le_drzava = QLineEdit()
        layout_left = QFormLayout()
        layout_left.addRow("Stevilka", self.le_stevilka)
        layout_left.addRow("Naziv", self.le_naziv)
        layout_left.addRow("Drzava", self.le_drzava)
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
                record = session.get(Posta, record_id)
                self.le_stevilka.setText(record.stevilka)
                self.le_naziv.setText(record.naziv)
                # self.le_drzava.setText(record.drzava)

    def prepare_add(self):
        self.record_id = None
        self.le_stevilka.setText("")
        self.le_naziv.setText("")
        self.le_drzava.setText("")

    def save_record(self):
        with Session(engine) as session:
            if self.record_id:
                record = session.get(Posta, self.record_id)
            else:
                record = Posta()
            record.naziv = self.le_naziv.text()
            record.stevilka = self.le_stevilka.text()
            record.drzava = 60
            if not self.record_id:
                session.add(record)
            session.commit()
            session.close()
