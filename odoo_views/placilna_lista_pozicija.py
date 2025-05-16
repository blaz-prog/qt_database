from generic_mvc_alchemy.generic_table_model import GenericTableModel
from sqlalchemy import select, bindparam
from sqlalchemy.orm import Session
from postgresql_engine.engine import engine, session
from app_models.app_tables import PlacilnaListaPozicija
from PyQt6.QtCore import QAbstractTableModel, Qt


class PlacilnaListaPozicijaModel(QAbstractTableModel):
    TITLE = "Pozicija plačilne lista"
    FIELDS_HEADERS = [
        ('vrsta_izplacila.naziv', 'Vrsta izplačila'),
        ('kolicina', 'Količina'),
        ('vrednost_na_enoto', 'Vrednost na em.'),
        ('osnova', "Osnova"),
        ('odstotek', "Odstotek"),
        ('skupaj', "Skupaj"),
    ]
    def __init__(self, placilna_lista=None):
        super().__init__()
        if placilna_lista:
            self.placilna_lista = placilna_lista
            self.pozicije = placilna_lista.pozicije
        else:
            self.pozicije = []

    def rowCount(self, parent=None):
        return len(self.pozicije)

    def columnCount(self, parent=None):
        return len(self.FIELDS_HEADERS)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or \
                not (0 <= index.row() < len(self.pozicije)):
            return None
        record = self.pozicije[index.row()]
        column = index.column()
        if role == Qt.ItemDataRole.DisplayRole.DisplayRole:
            field_name = self.FIELDS_HEADERS[column][0]
            fields = field_name.split('.')
            value = ""
            for field_name in fields:
                value = getattr(record, field_name)
                record = value
            return value

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.TextAlignmentRole:
            if orientation == Qt.Orientation.Horizontal:
                return Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
            return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            return self.FIELDS_HEADERS[section][1]
        # Vertikalno napisem stevilko vrstice
        return int(section + 1)

    def set_placilna_lista(self, placilna_lista):
        self.placilna_lista = placilna_lista
        self.pozicije = placilna_lista.pozicije



