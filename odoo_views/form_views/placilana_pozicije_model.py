import PyQt6.QtCore as qtc
from app_models.app_tables import PlacilnaLista, PlacilnaListaPozicija

from sqlalchemy.orm import DeclarativeBase

class PlacilnaPozicijeModel(qtc.QAbstractTableModel):

    def __init__(self, session, placilna_lista:PlacilnaLista):
        super().__init__()
        self.dirty = False
        self.db_session = session
        self.record_list = placilna_lista.pozicije
        self.fields_headers = PlacilnaListaPozicija.FIELDS_HEADERS

    def rowCount(self, parent=None):
        return len(self.record_list)

    def columnCount(self, parent=None):
        return len(self.fields_headers)

    def data(self, index, role=qtc.Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or \
                not (0 <= index.row() < len(self.record_list)):
            return None
        record = self.record_list[index.row()]
        column = index.column()
        if role == qtc.Qt.ItemDataRole.DisplayRole.DisplayRole:
            field_name = self.fields_headers[column][0]
            fields = field_name.split('.')
            value = ""
            for field_name in fields:
                value = getattr(record, field_name)
                record = value
            return value

    def headerData(self, section, orientation, role=qtc.Qt.ItemDataRole.DisplayRole):
        if role == qtc.Qt.ItemDataRole.TextAlignmentRole:
            if orientation == qtc.Qt.Orientation.Horizontal:
                return qtc.Qt.AlignmentFlag.AlignCenter | qtc.Qt.AlignmentFlag.AlignVCenter
            return qtc.Qt.AlignmentFlag.AlignRight | qtc.Qt.AlignmentFlag.AlignVCenter
        if role != qtc.Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == qtc.Qt.Orientation.Horizontal:
            return self.fields_headers[section][1]
        # Vertikalno napisem stevilko vrstice
        return int(section + 1)
