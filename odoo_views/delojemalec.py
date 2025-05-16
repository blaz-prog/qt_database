from generic_mvc_alchemy.generic_table_model import GenericTableModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from postgresql_engine.engine import engine, session
from app_models.app_tables import Delojemalec

class DelojemalecModel(GenericTableModel):
    TITLE = "Delojemalec"
    FIELDS_HEADERS = [
        ('ime', 'Ime'),
        ('priimek', 'Priimek'),
        ('davcna_stevilka', "Davčna številka"),
        ('ulica', "Ulica/Kraj"),
        ('posta', "Posta"),
        ('spol', "Spol")
    ]
    def __init__(self):
        super().__init__(session)
        self.search_filter = ''


    def query_data(self, search_filter):
        stmt = select(Delojemalec)
        if search_filter:
            stmt = stmt.where(
                (Delojemalec.priimek.ilike(f"{search_filter}%"))
            )
        stmt = stmt.order_by(Delojemalec.priimek)
        return session.scalars(stmt).all()

    def get_by_id(self, drzava_id):
        with Session(engine) as s:
            result = s.get(Delojemalec, drzava_id)
        if result:
            return result.name_get()
        else:
            return ""
