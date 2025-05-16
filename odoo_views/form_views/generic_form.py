import sys
from PyQt6.QtWidgets import (QWidget, QTableView, QVBoxLayout, QHBoxLayout,
                             QGroupBox, QLineEdit,QLabel, QTextEdit, QDialog, QComboBox,
                             QFormLayout, QGridLayout, QPushButton, QApplication, QHeaderView,
                             QDialogButtonBox, QMessageBox)


from app_models.app_tables import Delojemalec
from datetime import datetime
from sqlalchemy.orm import Session
from postgresql_engine.engine import engine

class RecordEditForm(QDialog):

    def __init__(self, parent=None, record_id = None):
        super().__init__(parent)
        self.record_list = []
        self.record_id = record_id
        self.controls_widget = QWidget(self)
        main_layout = QHBoxLayout()
        # ustvarim kontrole
        controls_layout = QVBoxLayout()
        self.btn_save = QPushButton('Shrani')
        self.btn_undo = QPushButton('Razveljavi')
        controls_layout.addWidget(self.btn_save)
        controls_layout.addWidget(self.btn_undo)
        controls_layout.addStretch()
        main_layout.addWidget(self.controls_widget)
        main_layout.addLayout(controls_layout)
        self.setLayout(main_layout)
        # signals & slots
        self.btn_save.clicked.connect(self.save_record)
        # housekeeping
        self.setGeometry(20, 20, 400, 500)


    def read_record(self, record_id):
        """
        Read record from database and show on form
        :param record_id:
        :return:
        """
        if record_id:
            self.record_id = record_id
            # self.setWindowTitle('Urejanje delojemalca')

    def prepare_add(self):
        pass

    def save_record(self):
        pass
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = RecordEditForm()
    mw.setWindowTitle('Generic Record Editing form')
    mw.show()
    sys.exit(app.exec())
