import sys
from PyQt6.QtWidgets import (QLineEdit,
                             QFormLayout, QVBoxLayout, QHBoxLayout, QTableView, QPushButton)

from app_models.app_tables import PlacilnaLista, PlacilnaListaPozicija, VrstaIzplacila
from sqlalchemy.orm import Session
from postgresql_engine.engine import engine
from .generic_form import RecordEditForm
from generic_mvc_alchemy.generic_lookup import DBLineEdit
from odoo_views.delojemalec import DelojemalecModel
# from odoo_views.placilna_lista_pozicija import PlacilnaListaPozicijaModel
from odoo_views.form_views.placilana_pozicije_model import PlacilnaPozicijeModel
from odoo_views.completers.db_completers import DelojemalecCompleter
from odoo_views.TableEditor import TableEditor
from odoo_views.form_views.pozicija_form import PozicijaForm

class PlacilnaListaForm(RecordEditForm):

    def __init__(self, parent=None, record_id = None):
        super().__init__(parent)
        self.form_session = Session(engine)
        self.record_list = []
        self.record_id = record_id
        if record_id:
            self.placilna_lista = self.form_session.get(PlacilnaLista, record_id)
        else:
            self.placilna_lista = PlacilnaLista()
        # ustvarim kontrole
        self.le_sklic = QLineEdit()
        self.le_delojemalec_id = DBLineEdit(DelojemalecModel, DelojemalecCompleter)
        self.le_datum_obracuna_od = QLineEdit()
        self.le_datum_obracuna_do = QLineEdit()
        self.le_datum_izplacila = QLineEdit()

        controls_layout = QVBoxLayout()
        edit_layout = QHBoxLayout()
        layout_left = QFormLayout()
        layout_left.addRow("Sklic", self.le_sklic)
        layout_left.addRow("Delojemalec", self.le_delojemalec_id)
        layout_right = QFormLayout()
        layout_right.addRow("Datum obračuna od", self.le_datum_obracuna_od)
        layout_right.addRow("Datum obračuna do", self.le_datum_obracuna_do)
        layout_right.addRow("Datum izplačila", self.le_datum_izplacila)
        edit_layout.addLayout(layout_left)
        edit_layout.addLayout(layout_right)
        controls_layout.addLayout(edit_layout)

        # gumbi za urejanje pozicij
        table_buttons_layout = QHBoxLayout()
        self.btn_poz_add = QPushButton("Dodaj pozicijo")
        self.btn_poz_delete = QPushButton("Izbriši pozicijo")
        self.btn_poz_recalculate = QPushButton("Preračunaj")
        table_buttons_layout.addWidget(self.btn_poz_add)
        table_buttons_layout.addWidget(self.btn_poz_delete)
        table_buttons_layout.addStretch()
        table_buttons_layout.addWidget(self.btn_poz_recalculate)
        self.btn_poz_add.clicked.connect(self.dodaj_pozicijo)
        self.btn_poz_delete.clicked.connect(self.brisi_pozicijo)
        self.btn_poz_recalculate.clicked.connect(self.recalculate)
        controls_layout.addLayout(table_buttons_layout)

        # Table view pozicije
        self.tw_pozicije = QTableView()
        self.pozicije_model = PlacilnaPozicijeModel(self.form_session, self.placilna_lista)
        self.tw_pozicije.setModel(self.pozicije_model)
        controls_layout.addWidget(self.tw_pozicije)
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
            self.setWindowTitle('Urejanje plačilne liste')
            record = self.form_session.get(PlacilnaLista, record_id)
            self.le_sklic.setText(record.sklic)
            self.le_delojemalec_id.db_value = record.delojemalec_id
            self.le_datum_obracuna_od.setText(record.datum_obracuna_od)
            self.le_datum_obracuna_do.setText(record.datum_obracuna_do)
            self.le_datum_izplacila.setText(record.datum_izplacila)
            self.placilna_lista = record
            # prebral sem novo placilno listo
            # moram spremeniti model za pozicije
            self.pozicije_model = PlacilnaPozicijeModel(self.form_session, self.placilna_lista)
            self.tw_pozicije.setModel(self.pozicije_model)
            self.pozicije_model.layoutChanged.emit()
        else:
            self.placilna_lista = PlacilnaLista()
            self.pozicije_model = PlacilnaPozicijeModel(self.form_session, self.placilna_lista)
            self.pozicije_model.layoutChanged.emit()

    def prepare_add(self):
        """
        pripravim vnosna polja za vnos novega in napisem
        morebitne privzete vrednosti
        :return:
        """
        self.record_id = None
        self.le_sklic.setText("")
        self.le_delojemalec_id.db_value = False
        self.le_datum_obracuna_od.setText("")
        self.le_datum_obracuna_do.setText("")
        self.le_datum_izplacila.setText("")

    def dodaj_pozicijo(self):
        print("Dodajam pozicije")
        dlg = PozicijaForm(self)
        dlg.prepare_add()
        if dlg.exec():
            print(dlg.le_vrsta_izplacila.db_value,  dlg.le_vrsta_izplacila.text(), dlg.le_kolicina.text())
            vi = self.form_session.get(VrstaIzplacila, dlg.le_vrsta_izplacila.db_value)
            pozicija = PlacilnaListaPozicija(vrsta_izplacila= vi,
                                  kolicina=float(dlg.le_kolicina.text()),
                                  vrednost_na_enoto=float(dlg.le_vrednost_na_enoto.text()),
                                  osnova=float(dlg.le_osnova.text()),
                                  odstotek=float(dlg.le_odstotek.text()),
                                  skupaj=float(dlg.le_skupaj.text())
                                  )
            print(pozicija.vrsta_izplacila)
            self.placilna_lista.pozicije.append(pozicija)
            print(len(self.placilna_lista.pozicije))
            self.pozicije_model.layoutChanged.emit()

    def brisi_pozicijo(self):
        print("Brisem pozicijo")

    def recalculate(self):
        print("Preracunavam...")

    def save_record(self):
        with Session(engine) as session:
            if self.record_id:
                record = session.get(PlacilnaLista, self.record_id)
            else:
                record = PlacilnaLista()

            record.sklic = self.le_sklic.text()
            record.delojemalec_id = self.le_delojemalec_id.db_value
            record.datum_obracuna_od = self.le_datum_obracuna_od.text()
            record.datum_obracuna_do = self.le_datum_obracuna_do.text()
            record.datum_izplacila = self.le_datum_izplacila.text()
            if not self.record_id:
                session.add(record)
            session.commit()
            session.close()

    def closeEvent(self, event):
        self.form_session.close()
        event.accept()
