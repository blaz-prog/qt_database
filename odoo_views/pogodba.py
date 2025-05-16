from generic_mvc_alchemy.generic_table_model import GenericTableModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from postgresql_engine.engine import engine, session
from app_models.app_tables import Pogodba

class PogodbaModel(GenericTableModel):
    TITLE = "Poste"
    FIELDS_HEADERS = [
        ('delojemalec_id', 'Ident'),
        ('delojemalec.ime', 'Ime'),
        ('delojemalec.priimek', 'Priimek'),
        ('urna_postavka', 'Urinina red. del.'),
        ('urna_postavka_refundacije', 'Urnina ref.'),
        ('povprecje_1m', 'Povprečje 1m'),
        ('povprecje_3m', 'Povprečje 3m'),
        ('leta_delovne_dobe', 'Del. doba. let'),
        ('tedenska_delovna_obveznost', 'Ur v tednu'),
    ]
    def __init__(self):
        super().__init__(session)
        self.search_filter = ''


    def query_data(self, search_filter):
        stmt = select(Pogodba)
        if search_filter:
            stmt = stmt.where(
                (Pogodba.delojemalec.priimek.ilike(f"{search_filter}%"))
            )
        # stmt = stmt.order_by(Pogodba.delojemalec.naziv)
        return session.scalars(stmt).all()

    def get_by_id(self, _id):
        with Session(engine) as s:
            result = s.get(Pogodba, _id)

        if result:
            return result.name_get()
        else:
            return ""
