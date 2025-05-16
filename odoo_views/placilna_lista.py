from generic_mvc_alchemy.generic_table_model import GenericTableModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from postgresql_engine.engine import engine, session
from app_models.app_tables import PlacilnaLista


class PlacilnaListaModel(GenericTableModel):
    TITLE = "Plačilna lista"
    FIELDS_HEADERS = [
        ('sklic', 'Sklic'),
        ('delojemalec.ime', 'Ime'),
        ('delojemalec.priimek', 'Priimek'),
        ('datum_obracuna_od', "Obračun od"),
        ('datum_obracuna_do', "Obračun do"),
        ('datum_izplacila', "Datum izplačila"),
    ]
    def __init__(self):
        super().__init__(session)
        self.search_filter = ''


    def query_data(self, search_filter):
        stmt = select(PlacilnaLista)
        if search_filter:
            stmt = stmt.where(
                (PlacilnaLista.delojemalec.priimek.ilike(f"{search_filter}%"))
            )
        stmt = stmt.order_by(PlacilnaLista.datum_obracuna_od)
        return session.scalars(stmt).all()

    def get_by_id(self, _id):
        with Session(engine) as s:
            result = s.get(PlacilnaLista, _id)
        if result:
            return result.name_get()
        else:
            return ""
