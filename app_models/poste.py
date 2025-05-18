from app_models.app_tables import Base, engine

from sqlalchemy import ForeignKey, Integer, String, select, bindparam, Select,  text
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime

class Posta(Base):
    __tablename__ = 'posta'
    id: Mapped[int] = mapped_column(primary_key=True)
    stevilka: Mapped[str]
    naziv: Mapped[str]

    def name_get(self):
        return f"{self.stevilka} {self.naziv}"

    def id_get(self):
        return self.id

    @staticmethod
    def get_number_of_matches(filter_text):
        '''
        Return number of matches for filter
        :param filter_text:
        :return:
        '''
        with Session(engine) as select_session:
            stmt = text("""
            SELECT count(*) FROM posta WHERE naziv ilike :filter
            """)
            stmt = stmt.bindparams(filter = f"{filter_text}%")
            num_rec = select_session.execute(stmt).scalar()
            return num_rec

    @staticmethod
    def get_matches(filter_text):
        '''
        return matches for filter_text
        :param filter_text:
        :return:
        '''
        with Session(engine) as select_session:
            stmt = select(Posta).where(Posta.naziv.ilike(f"{filter_text}%"))
            results = select_session.scalars(stmt).all()
            return [(res.naziv, res.id) for res in results]

    @staticmethod
    def get_exact_match(filter_text):
        with Session(engine) as select_session:
            stmt = select(Posta).where(Posta.naziv == filter_text)
            result = select_session.scalars(stmt).first()
            if result:
                return result.id
            else:
                return None

