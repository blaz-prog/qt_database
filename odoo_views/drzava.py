from generic_mvc_alchemy.generic_table_model import GenericTableModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from postgresql_engine.engine import engine, session
from app_models.app_tables import Drzava

class DrzavaModel(GenericTableModel):
    TITLE = "Poste"
    FIELDS_HEADERS = [
        ('iso_koda', 'Iso koda'),
        ('naziv', 'Naziv'),
    ]
    def __init__(self):
        super().__init__(session)
        self.search_filter = ''


    def query_data(self, search_filter, exact=False):
        stmt = select(Drzava)
        if search_filter:
            if exact:
                stmt = stmt.where(
                    (Drzava.naziv == (f"{search_filter}"))
                )
            else:
                stmt = stmt.where(
                    (Drzava.naziv.ilike(f"{search_filter}%"))
                )
        stmt = stmt.order_by(Drzava.naziv)
        return session.scalars(stmt).all()

    def get_by_id(self, drzava_id):
        with Session(engine) as s:
            result = s.get(Drzava, drzava_id)
        if result:
            return result.name_get()
        else:
            return ""
