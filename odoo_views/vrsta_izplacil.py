from generic_mvc_alchemy.generic_table_model import GenericTableModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from postgresql_engine.engine import engine, session
from app_models.app_tables import VrstaIzplacila

class VrstaIzplacilaModel(GenericTableModel):
    TITLE = "Kategorije izplačila"
    FIELDS_HEADERS = [
        ('oznaka', 'Oznaka'),
        ('naziv', 'Naziv'),
        ('kategorija.naziv', 'Kategorija'),
    ]
    def __init__(self):
        super().__init__(session)
        self.search_filter = ''


    def query_data(self, search_filter):
        stmt = select(VrstaIzplacila)
        if search_filter:
            stmt = stmt.where(
                (VrstaIzplacila.naziv.ilike(f"{search_filter}%"))
            )
        stmt = stmt.order_by('oznaka')
        return session.scalars(stmt).all()

    def get_by_id(self, _id):
        with Session(engine) as s:
            result = s.get(VrstaIzplacila, _id)

        if result:
            return result.name_get()
        else:
            return ""

