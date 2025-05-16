import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QMdiArea, QMdiSubWindow
from PyQt6.QtGui import QAction
from app_views.poste_view import PostaView


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
        self.setWindowTitle('Statusbar')
        menubar = self.menuBar()
        newAction = QAction('Delojemalci', self)
        newAction.triggered.connect(self.pokazi_delojemalce)

        editAction = QAction('Pogodbe', self)
        editAction.triggered.connect(self.pokazi_pogodbe)
        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(self.close)
        fileMenu = menubar.addMenu('Matični podatki')
        fileMenu.addAction(newAction)
        fileMenu.addAction(editAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        fileSifranti = menubar.addMenu('Šifranti')
        posteAction = QAction('Pošte', self)
        posteAction.triggered.connect(self.pokazi_poste)
        drzaveAction = QAction('Države', self)
        drzaveAction.triggered.connect(self.pokazi_drzave)
        fileSifranti.addAction(posteAction)
        fileSifranti.addAction(drzaveAction)

        self.setGeometry(300, 300, 800, 600)
        # End menu items
        self.show()

    def pokazi_delojemalce(self):
        print('pokazi_delojemalce')

    def pokazi_pogodbe(self):
        print('pokazi_pogodbe')

    def pokazi_poste(self):
        sub = QMdiSubWindow()
        pw = PostaView()
        sub.setWidget(pw)
        sub.maximumSize()
        self.mdi.addSubWindow(sub)
        sub.showMaximized()

    def pokazi_drzave(self):
        print('pokazi_drzave')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = MainWindow()
    sys.exit(app.exec())
