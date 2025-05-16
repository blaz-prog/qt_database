import sys
from functools import partial
from PyQt6.QtWidgets import QMainWindow, QApplication, QMdiArea, QMdiSubWindow
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (QWidget, QTableView, QVBoxLayout, QHBoxLayout,
                             QGroupBox, QLineEdit,
                             QPushButton, QApplication, QHeaderView,
                             QMessageBox, QStackedWidget, QLabel)


from delojemalec import DelojemalecModel
from posta import PostaModel
from drzava import DrzavaModel
from pogodba import PogodbaModel
from kategorija_izplacila import KategorijaIzplacilaModel
from vrsta_izplacil import VrstaIzplacilaModel
from placilna_lista import PlacilnaListaModel

from form_views.delojemalec_form import DelojemalecForm
from form_views.poste_form import PostaForm
from form_views.drzava_form import DrzavaForm
from form_views.pogodba_form import PogodbaForm
from form_views.kategorija_vrste_izplacil import KategorijaIzplacilForm
from form_views.vrsta_izplacil_form import VrstaIzplacilaForm
from form_views.placilna_lista_form import PlacilnaListaForm
from TableEditor import TableEditor


class MainWindow(QMainWindow):
    def __init__(self):
        """MainWindow constructor.

        This widget will be our main window.
        We'll define all the UI components in here.
        """
        super().__init__()
        # Main UI code goes here
        self.setWindowTitle("Kadri")
        self.setGeometry(300, 300, 800, 600)
        # End main UI code
        # Menu items

        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)
        self.setWindowTitle('Kadri')
        menubar = self.menuBar()
        newAction = QAction('Delojemalci', self)
        newAction.triggered.connect(self.pokazi_delojemalce)

        editAction = QAction('Pogodbe', self)
        editAction.triggered.connect(self.pokazi_pogodbe)

        placilne_action = QAction("Plačilne liste", self)
        placilne_action.triggered.connect(self.pokazi_placilne_liste)

        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(self.close)
        fileMenu = menubar.addMenu('Matični podatki')
        fileMenu.addAction(newAction)
        fileMenu.addAction(editAction)
        fileMenu.addAction(placilne_action)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        # Nastavitve osnovnih podatkov
        fileSifranti = menubar.addMenu('Šifranti')
        posteAction = QAction('Pošte', self)
        posteAction.triggered.connect(self.pokazi_poste)
        drzaveAction = QAction('Države', self)
        drzaveAction.triggered.connect(self.pokazi_drzave)
        fileSifranti.addAction(posteAction)
        fileSifranti.addAction(drzaveAction)

        # Nastavitve obračuna
        mnu_nastavitve_obracun = menubar.addMenu("Nastavitve obračun")
        kategorije = QAction("Kategorije izplačil", self)
        vrste_izplacil = QAction("Vrste izplačil", self)
        mnu_nastavitve_obracun.addAction(kategorije)
        mnu_nastavitve_obracun.addAction(vrste_izplacil)
        kategorije.triggered.connect(self.pokazi_kategorije)
        vrste_izplacil.triggered.connect(self.pokazi_vrste_izplacil)

        self.windows_menu = menubar.addMenu("Window")
        self.tileAction = QAction("Tile", self)
        self.tileAction.triggered.connect(self.tile_windows)
        self.windows_menu.addAction(self.tileAction)
        self.windows_menu.aboutToShow.connect(self.update_window_menu)

        self.setGeometry(300, 300, 800, 600)
        # End menu items
        self.showMaximized()

    def pokazi_delojemalce(self):
        self.show_subwindow(DelojemalecModel, DelojemalecForm, 'Delojemalci')

    def pokazi_pogodbe(self):
        self.show_subwindow(PogodbaModel, PogodbaForm, 'Pogodbe')

    def pokazi_placilne_liste(self):
        self.show_subwindow(PlacilnaListaModel, PlacilnaListaForm, 'Plačilne Liste')


    def pokazi_poste(self):
        self.show_subwindow(PostaModel, PostaForm, 'Pošte')

    def pokazi_drzave(self):
        self.show_subwindow(DrzavaModel, DrzavaForm, 'Države')

    def pokazi_kategorije(self):
        self.show_subwindow(KategorijaIzplacilaModel,
                            KategorijaIzplacilForm,
                            'Kategorije izplačil')

    def pokazi_vrste_izplacil(self):
        self.show_subwindow(VrstaIzplacilaModel,
                            VrstaIzplacilaForm,
                            'Vrste izplačil')

    def tile_windows(self):
        self.mdi.tileSubWindows()

    def show_subwindow(self, model, form, title):
        sub = QMdiSubWindow()
        mw = TableEditor(model, form)
        mw.setWindowTitle(title)
        sub.setWidget(mw)
        init_geometry = TableEditor.read_settings()
        sub.setGeometry(init_geometry)

        self.mdi.addSubWindow(sub)
        sub.show()

    def update_window_menu(self):
        self.windows_menu.clear()
        self.windows_menu.addAction(self.tileAction)
        mdi_subwindows = self.mdi.subWindowList()
        if not mdi_subwindows:
            return
        self.windows_menu.addSeparator()
        for sub_window in mdi_subwindows:
            if sub_window.isMinimized() or sub_window.isVisible():
                title = sub_window.windowTitle()
                action = self.windows_menu.addAction(title)
                partial_func = partial(self.set_active_window, sub_window)
                action.triggered.connect(partial_func)

    def set_active_window(self, window):
        self.mdi.setActiveSubWindow(window)

if __name__ == '__main__':
    # za bazo uporabljam qt in sqlqlchemy.
    # tu je priklop prek qt.
    from PyQt6.QtSql import QSqlDatabase
    db = QSqlDatabase.addDatabase("QPSQL")
    db.setUserName('blaz')
    db.setPassword('buratino')
    db.setDatabaseName('kadri')
    if not db.open():
        print("Unable to open database.")
    else:
        print("Database successfully opened.")
    # Nastavitve programa
    QApplication.setOrganizationName("Lastovka")
    QApplication.setApplicationName("OdooClone")
    app = QApplication(sys.argv)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = MainWindow()
    sys.exit(app.exec())
