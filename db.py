import os
from PyQt6.QtSql import QSqlDatabase
db = QSqlDatabase.addDatabase("QPSQL")
db.setUserName('blaz')
db.setPassword('buratino')
db.setDatabaseName('kadri')
if not db.open():
    print("Unable to open database.")
else:
    print("Database successfully opened.")