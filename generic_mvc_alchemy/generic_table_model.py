import PyQt6.QtCore as qtc
from sqlalchemy.orm import DeclarativeBase

class GenericTableModel(qtc.QAbstractTableModel):

    '''
    genericni model za pregledovanje tabel
    v dedovanem razredu je potrebno nastaviti FIELDS_HEADERS
    '''
    FIELDS_HEADERS = [
        # Enter field headers here
        ('code', 'Code'),
        ('name', 'Name'),
    ]

    def __init__(self, session):
        super().__init__()
        self.dirty = False
        self.db_session = session
        self.record_list = []

    def rowCount(self, parent=None):
        return len(self.record_list)

    def columnCount(self, parent=None):
        return len(self.FIELDS_HEADERS)

    def data(self, index, role=qtc.Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or \
                not (0 <= index.row() < len(self.record_list)):
            return None
        record = self.record_list[index.row()]
        column = index.column()
        if role == qtc.Qt.ItemDataRole.DisplayRole.DisplayRole:
            field_name = self.FIELDS_HEADERS[column][0]
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
            return self.FIELDS_HEADERS[section][1]
        # Vertikalno napisem stevilko vrstice
        return int(section + 1)


    def add(self, record):
        # dodam v bazo in posodobim gui
        self.db_session.add(record)
        self.db_session.commit()
        self.record_list.append(record)
        self.layoutChanged.emit()

    def delete_record(self, record_index):
        # izbrisem iz baze in iz liste, ki jo prikazujem na formi
        record = self.record_list[record_index]
        self.db_session.delete(record)
        self.db_session.commit()
        self.record_list.pop(record_index)
        self.layoutChanged.emit()

    def load(self, search_filter=''):
        '''
        nalozim model in javim spremembo view-u
        :param search_filter:
        :return:
        '''
        self.record_list = []
        self.record_list = self.query_data(search_filter)
        self.layoutChanged.emit()

    def set_search_filter(self, search_filter):
        self.query_data(search_filter)

    def query_data(self, search_filter, exact=False):
        pass
