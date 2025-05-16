import sys
from PyQt6.QtWidgets import  (QLineEdit,
                              QFormLayout, QHBoxLayout)

from app_models.app_tables import Pogodba
from sqlalchemy.orm import Session
from postgresql_engine.engine import engine
from .generic_form import RecordEditForm
from generic_mvc_alchemy.generic_lookup import DBLineEdit
from odoo_views.delojemalec import DelojemalecModel
from odoo_views.completers.db_completers import DelojemalecCompleter

class PogodbaForm(RecordEditForm):

    def __init__(self, parent=None, record_id = None):
        super().__init__(parent)
        self.record_list = []
        self.record_id = record_id
        # ustvarim kontrole
        self.le_delojemalec_id = DBLineEdit(DelojemalecModel, DelojemalecCompleter)
        self.le_urna_postavka = QLineEdit()
        self.le_urna_postavka_refundacije = QLineEdit()
        self.le_povprecje_1m = QLineEdit()
        self.le_povprecje_3m = QLineEdit()
        self.le_zaposlen_v_podjetju = QLineEdit()
        self.le_leta_delovne_dobe = QLineEdit()
        self.le_tedenska_delovna_obveznost  = QLineEdit()
        edit_layout = QHBoxLayout()
        layout_left = QFormLayout()
        layout_left.addRow("Delojemalec", self.le_delojemalec_id)
        layout_left.addRow("Zaposlen od", self.le_zaposlen_v_podjetju)
        layout_left.addRow("Leta delovne dobe", self.le_leta_delovne_dobe)
        layout_left.addRow("Tedenska obveznost", self.le_tedenska_delovna_obveznost)
        layout_right = QFormLayout()
        layout_right.addRow("Urna postavka", self.le_urna_postavka)
        layout_right.addRow("Urna postavka refundacije", self.le_urna_postavka_refundacije)
        layout_right.addRow("Povprečje 1m", self.le_povprecje_1m)
        layout_right.addRow("Povprečje 3m", self.le_povprecje_3m)
        edit_layout.addLayout(layout_left)
        edit_layout.addLayout(layout_right)
        self.controls_widget.setLayout(edit_layout)
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
                record = session.get(Pogodba, record_id)
                self.le_delojemalec_id.db_value = record.delojemalec_id
                self.le_urna_postavka.setText(str(record.urna_postavka))
                self.le_urna_postavka_refundacije.setText(str(record.urna_postavka_refundacije))
                self.le_povprecje_1m.setText(str(record.povprecje_1m))
                self.le_povprecje_3m.setText(str(record.povprecje_3m))
                self.le_zaposlen_v_podjetju.setText(str(record.zaposlen_v_podjetju))
                self.le_leta_delovne_dobe.setText(str(record.leta_delovne_dobe))
                self.le_tedenska_delovna_obveznost.setText(str(record.tedenska_delovna_obveznost))

    def prepare_add(self):
        """
        pripravim vnosna polja za vnos novega in napisem
        morebitne privzete vrednosti
        :return:
        """
        self.record_id = None
        self.le_delojemalec_id.db_value = False
        self.le_urna_postavka.setText("")
        self.le_urna_postavka_refundacije.setText("")
        self.le_povprecje_1m.setText("")
        self.le_povprecje_3m.setText("")
        self.le_zaposlen_v_podjetju.setText("")
        self.le_leta_delovne_dobe.setText("")

    def save_record(self):
        with Session(engine) as session:
            if self.record_id:
                record = session.get(Pogodba, self.record_id)
            else:
                record = Pogodba()

            record.delojemalec_id = self.le_delojemalec_id.db_value
            record.urna_postavka = float(self.le_urna_postavka.text())
            record.urna_postavka_refundacije = float(self.le_urna_postavka_refundacije.text())
            record.povprecje_1m = float(self.le_povprecje_1m.text())
            record.povprecje_3m = float(self.le_povprecje_3m.text())
            record.zaposlen_v_podjetju = self.le_zaposlen_v_podjetju.text()
            record.leta_delovne_dobe = int(self.le_leta_delovne_dobe.text())
            record.tedenska_delovna_obveznost = int(self.le_tedenska_delovna_obveznost.text())
            if not self.record_id:
                session.add(record)
            session.commit()
            session.close()
