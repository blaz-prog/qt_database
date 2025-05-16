from generic_mvc_alchemy.generic_table_model import GenericTableModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from postgresql_engine.engine import engine, session
from app_models.app_tables import Posta

class PostaModel(GenericTableModel):
    TITLE = "Poste"
    FIELDS_HEADERS = [
        ('stevilka', 'Stevilka'),
        ('naziv', 'Naziv'),
    ]
    def __init__(self):
        super().__init__(session)
        self.search_filter = ''


    def query_data(self, search_filter):
        stmt = select(Posta)
        if search_filter:
            stmt = stmt.where(
                (Posta.naziv.ilike(f"{search_filter}%"))
            )
        stmt = stmt.order_by(Posta.naziv)
        return session.scalars(stmt).all()

    def get_by_id(self, posta_id):
        with Session(engine) as s:
            result = s.get(Posta, posta_id)

        if result:
            return result.name_get()
        else:
            return ""

