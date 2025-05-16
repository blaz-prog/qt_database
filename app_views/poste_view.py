import sys
from PyQt6.QtCore import Qt, QEvent, QSortFilterProxyModel, QByteArray
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QApplication,
                             QWidget,
                             QDialogButtonBox,
                             QTableView,
                             QLineEdit,
                             QComboBox, QCompleter,
                             QPushButton,
                             QVBoxLayout, QFormLayout,
                             QHBoxLayout,
                             QStackedWidget,
                             QTableView,
                             QDataWidgetMapper, QItemDelegate,
                             QMessageBox, QSizePolicy, QAbstractItemView, QHeaderView
                             )

from PyQt6.QtSql import (QSqlDatabase, QSqlQuery,
                         QSqlQueryModel, QSqlTableModel,
                         QSqlRelationalTableModel, QSql,
                         QSqlRelation, QSqlRelationalDelegate)
from db_line_edit import DBLineEdit
import db


WINDOW_TITLE = 'Seznam pošt'
WINDOW_GEOMETRY = (300, 300, 500, 350)
class Delegate(QItemDelegate):

    def setEditorData(self, editor, index):
        if type(editor) == DBLineEdit:
            sql  = f"SELECT naziv FROM drzava where id = :drzava_id"
            query = QSqlQuery()
            query.prepare(sql)
            query.bindValue(":drzava_id", index.data())
            query.exec()
            while query.next():
                editor.setText(query.value(0))
            return
        super().setEditorData(editor, index)


    def setModelData(self, editor, model, index):
        if type(editor) == DBLineEdit:
            print("Setting DBLineEdit model data", editor.db_value)
        super().setModelData(editor, model, index)

class PostaForm(QWidget):
    """Form to display/edit all info about a post"""
    ADD_MODE = 1
    EDIT_MODE = 2
    def __init__(self, parent, model):
        super().__init__(parent)
        self.parent = parent
        self.edit_mode = 0
        self.model = model
        main_layout = QVBoxLayout()
        form_layout = QFormLayout()
        self.stevilka = QLineEdit()
        self.naziv = QLineEdit()
        self.drzava = DBLineEdit()

        # mapping
        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.model)
        self.mapper.setItemDelegate(Delegate(self))
        self.mapper.addMapping(self.stevilka, 1)
        self.mapper.addMapping(self.naziv, 2)
        self.mapper.addMapping(self.drzava, 3)

        form_layout.addRow('Številka', self.stevilka)
        form_layout.addRow('Naziv', self.naziv)
        form_layout.addRow('Drzava', self.drzava)
        main_layout.addLayout(form_layout)
        buttons_layout = QHBoxLayout()
        save_button = QPushButton('Shrani')
        back_button = QPushButton('Nazaj')
        back_button.clicked.connect(self.change_current_widget)
        save_button.clicked.connect(self.save_posta)
        buttons_layout.addWidget(save_button)
        buttons_layout.addStretch()
        buttons_layout.addWidget(back_button)
        main_layout.addLayout(buttons_layout)
        main_layout.addStretch()
        self.setLayout(main_layout)

    def change_current_widget(self):
        self.parent.stacked_widget.setCurrentWidget(self.parent.posta_tv)


    def add_record(self):
        self.edit_mode = PostaForm.ADD_MODE
        row = self.model.rowCount()
        self.mapper.submit()
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)
        self.stevilka.setFocus()

    def show_posta(self, model_index_row):
        self.edit_mode = PostaForm.EDIT_MODE
        '''
        v bistvu rabim samo model index, ker delam z mapperjem
        :param posta_data:
        :return:
        '''
        # self.id = posta_data.get('id')
        # self.stevilka.setText(posta_data.get('stevilka'))
        # self.naziv.setText(posta_data.get('naziv'))
        self.mapper.setCurrentIndex(model_index_row)
        print(self.mapper.currentIndex())

    def save_posta(self):
        self.mapper.submit()
        self.change_current_widget()
        # ssql = """
        # UPDATE posta SET stevilka = :stevilka, naziv = :naziv WHERE id = :id;
        # """
        # query = QSqlQuery(db.db)
        # query.prepare(ssql)
        # query.bindValue(':id', self.id)
        # query.bindValue(':stevilka', self.stevilka.text())
        # query.bindValue(':naziv', self.naziv.text())
        # query.exec()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Escape:
                self.change_current_widget()


class PostaView(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(*WINDOW_GEOMETRY)
        self.stacked_widget = QStackedWidget()
        main_layout = QVBoxLayout()
        self.le_search = QLineEdit()
        main_layout.addWidget(self.le_search)
        main_layout.addWidget(self.stacked_widget)

        # tabelaricni seznam post
        self.poste = QSqlQueryModel()
        self.query = """
            select p.id, p.stevilka, p.naziv, p.drzava_id, d.naziv  from posta p 
            inner join drzava d on p.drzava_id = d.id
            order by stevilka
        """
        self.poste.setQuery(self.query)
        # poste.setRelation(
        #     poste.fieldIndex('drzava_id'),
        #     QSqlRelation('drzava', 'id', 'naziv')
        # )

        self.poste.setHeaderData(1, Qt.Orientation.Horizontal, 'Številka')
        self.poste.setHeaderData(2, Qt.Orientation.Horizontal, 'Naziv')

        self.posta_tv = QTableView()
        self.posta_tv.setModel(self.poste)
        self.posta_tv.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.posta_tv.horizontalHeader().setSectionHidden(0, True)
        self.posta_tv.resizeColumnToContents(0)
        self.posta_tv.installEventFilter(self)
        self.posta_tv.hideColumn(0)
        self.posta_tv.hideColumn(3)
        self.posta_form = PostaForm(self, self.poste)
        self.stacked_widget.addWidget(self.posta_tv)
        self.stacked_widget.addWidget(self.posta_form)
        self.stacked_widget.setCurrentWidget(self.posta_tv)
        self.setLayout(main_layout)
        # buttons
        btn_add = QPushButton('Nov')
        btn_delete = QPushButton('Briši')
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(btn_add)
        buttons_layout.addWidget(btn_delete)
        main_layout.addLayout(buttons_layout)
        btn_add.clicked.connect(self.add_record)
        # signals and slots
        self.posta_tv.doubleClicked.connect(lambda x: self.show_posta(self.get_id_for_row(x)))
        self.le_search.textChanged.connect(self.filter_table)
        # hauskeeping
        self.posta_tv.setFocus()

    def eventFilter(self, obj, event):
        if obj == self.posta_tv:
            if  event.type() == QEvent.Type.KeyPress:
                if event.key() == Qt.Key.Key_Return:
                    current_row_index = self.posta_tv.currentIndex()
                    posta_id = self.get_id_for_row(current_row_index)
                    self.show_posta(posta_id)
        return super(PostaView, self).eventFilter(obj, event)

    def get_id_for_row(self, index):
        id_index = index.siblingAtColumn(0)
        posta_id = self.posta_tv.model().data(id_index)
        return posta_id

    def filter_table(self):
        filter_text = self.le_search.text()
        self.posta_tv.model().setFilter(f"naziv ilike '{filter_text}%'")
    def show_posta(self, posta_id):
        # query = QSqlQuery(db.db)
        # query.prepare('SELECT id, stevilka, naziv FROM posta WHERE id=:id')
        # query.bindValue(':id', posta_id)
        # query.exec()
        # query.next()
        # posta = {
        #     'id': query.value(0),
        #     'stevilka': query.value(1),
        #     'naziv': query.value(2)
        # }
        current_row_index = self.posta_tv.currentIndex()
        self.posta_form.show_posta(current_row_index.row())
        self.stacked_widget.setCurrentWidget(self.posta_form)

    def add_record(self):
        self.posta_form.add_record()
        self.stacked_widget.setCurrentWidget(self.posta_form)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    poste = PostaView()
    poste.show()
    sys.exit(app.exec())
