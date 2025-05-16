import sys
from PyQt6.QtWidgets import  (QLineEdit,
                             QFormLayout)

from app_models.app_tables import KategorijaIzplacila
from sqlalchemy.orm import Session
from postgresql_engine.engine import engine
from .generic_form import RecordEditForm

class KategorijaIzplacilForm(RecordEditForm):

    def __init__(self, parent=None, record_id = None):
        super().__init__(parent)
        self.record_list = []
        self.record_id = record_id
        # ustvarim kontrole
        self.le_oznaka = QLineEdit()
        self.le_naziv = QLineEdit()
        layout_left = QFormLayout()
        layout_left.addRow("Oznaka", self.le_oznaka)
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
            self.setWindowTitle('Urejanje kategorij')
            with Session(engine) as session:
                record = session.get(KategorijaIzplacila, record_id)
                self.le_oznaka.setText(record.oznaka)
                self.le_naziv.setText(record.naziv)
                # self.le_drzava.setText(record.drzava)

    def prepare_add(self):
        self.record_id = None
        self.le_oznaka.setText("")
        self.le_naziv.setText("")

    def save_record(self):
        with Session(engine) as session:
            if self.record_id:
                record = session.get(KategorijaIzplacila, self.record_id)
            else:
                record = KategorijaIzplacila()
            record.oznaka = self.le_oznaka.text()
            record.naziv = self.le_naziv.text()
            if not self.record_id:
                session.add(record)
            session.commit()
            session.close()
