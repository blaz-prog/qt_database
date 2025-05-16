import sys
from PyQt6.QtWidgets import  (QLineEdit,
                              QFormLayout, QHBoxLayout)

from app_models.app_tables import PlacilnaLista, PlacilnaListaPozicija
from sqlalchemy.orm import Session
from postgresql_engine.engine import engine
from .generic_form import RecordEditForm
from generic_mvc_alchemy.generic_lookup import DBLineEdit
from odoo_views.vrsta_izplacil import VrstaIzplacilaModel
from odoo_views.completers.db_completers import VrstaIzplacilaCompleter

class PozicijaForm(RecordEditForm):

    def __init__(self, parent=None, record_id = None):
        super().__init__(parent)
        self.record_list = []
        self.record_id = record_id
        # ustvarim kontrole
        self.le_vrsta_izplacila = DBLineEdit(VrstaIzplacilaModel, VrstaIzplacilaCompleter)
        self.le_kolicina = QLineEdit()
        self.le_vrednost_na_enoto = QLineEdit()
        self.le_osnova = QLineEdit()
        self.le_odstotek = QLineEdit()
        self.le_skupaj = QLineEdit()
        edit_layout = QHBoxLayout()
        layout_left = QFormLayout()

        layout_left.addRow("Vrsta izplačila", self.le_vrsta_izplacila)
        layout_left.addRow("Kolicina", self.le_kolicina)
        layout_left.addRow("Vrednost enota",self.le_vrednost_na_enoto)
        layout_left.addRow("Osnova",self.le_osnova)
        layout_left.addRow("Odstotek",self.le_odstotek)
        layout_left.addRow("Skupaj",self.le_skupaj)
        edit_layout.addLayout(layout_left)
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
            # with Session(engine) as session:
            #     record = session.get(PlacilnaLista, record_id)
            #     self.le_sklic.setText(record.sklic)
            #     self.le_delojemalec_id.db_value = record.delojemalec_id
            #     self.le_datum_obracuna_od.setText(record.datum_obracuna_od)
            #     self.le_datum_obracuna_do.setText(record.datum_obracuna_do)
            #     self.le_datum_izplacila.setText(record.datum_izplacila)

    def prepare_add(self):
        """
        pripravim vnosna polja za vnos novega in napisem
        morebitne privzete vrednosti
        :return:
        """
        self.record_id = None
        self.le_vrsta_izplacila.db_value = False
        self.le_kolicina.setText("")
        self.le_vrednost_na_enoto.setText("")
        self.le_osnova.setText("")
        self.le_odstotek.setText("")

    def save_record(self):
        self.accept()
