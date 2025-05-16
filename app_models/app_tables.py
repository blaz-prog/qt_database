from sqlalchemy import ForeignKey, Integer, String, select, bindparam, Select
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
from postgresql_engine.engine import engine, session


class Base(DeclarativeBase):
    pass


class Posta(Base):
    __tablename__ = 'posta'
    id: Mapped[int] = mapped_column(primary_key=True)
    stevilka: Mapped[str]
    naziv: Mapped[str]

    def name_get(self):
        return f"{self.stevilka} {self.naziv}"

    def id_get(self):
        return self.id


class Drzava(Base):
    __tablename__ = 'drzava'
    id: Mapped[int] = mapped_column(primary_key=True)
    iso_koda: Mapped[str]
    naziv: Mapped[str]

    def name_get(self):
        return self.naziv

    def id_get(self):
        return self.id


class Delojemalec(Base):
    __tablename__ = "delojemalec"

    id: Mapped[int] = mapped_column(primary_key=True)
    ime: Mapped[str]
    priimek: Mapped[str]
    ulica: Mapped[str]
    drzava: Mapped[str]
    datum_rojstva: Mapped[datetime.date]
    davcna_stevilka: Mapped[str]
    emso: Mapped[str]
    spol: Mapped[str]
    posta: Mapped[int] = mapped_column(ForeignKey("posta.id"),
                                       nullable=False)
    drzava_id: Mapped[int] = mapped_column(ForeignKey("drzava.id"),
                                           nullable=False)
    pogodbe: Mapped[list["Pogodba"]] = relationship(back_populates="delojemalec",
                                                    cascade="all, delete-orphan")

    otroci: Mapped[list["Otrok"]] = relationship(back_populates="delojemalec",
                                                 cascade="all, delete-orphan")

    placilne_liste: Mapped[list["PlacilnaLista"]] = relationship(back_populates="delojemalec",
                                                                 cascade="all, delete-orphan")

    def __str__(self):
        return f"{self.ime} {self.priimek}"

    def name_get(self):
        return f"{self.ime} {self.priimek}"

    def id_get(self):
        return self.id


class Otrok(Base):
    __tablename__ = 'otrok'
    id: Mapped[int] = mapped_column(primary_key=True)
    ime: Mapped[str] = mapped_column(String(50))
    starost: Mapped[int]
    delojemalec_id: Mapped[int] = mapped_column(ForeignKey("delojemalec.id"), nullable=False)
    delojemalec: Mapped["Delojemalec"] = relationship(back_populates="otroci")

    FIELDS_HEADERS = [
        ('ime', 'Ime'),
        ('starost', 'Starost')
    ]

    def name_get(self):
        return f"{self.ime}"

    def id_get(self):
        return self.id

    def __str__(self):
        return self.name_get()

    @classmethod
    def get_recordset(cls):
        stmt = Select(Otrok)
        result = session.scalars(stmt).all()
        for r in result:
            print(r)


class Pogodba(Base):
    __tablename__ = "pogodba"
    id: Mapped[int] = mapped_column(primary_key=True)
    delojemalec_id: Mapped[int] = mapped_column(ForeignKey("delojemalec.id"), nullable=False)
    delojemalec: Mapped["Delojemalec"] = relationship(back_populates="pogodbe")
    urna_postavka: Mapped[float]
    urna_postavka_refundacije: Mapped[float]
    povprecje_1m: Mapped[float]
    povprecje_3m: Mapped[float]
    zaposlen_v_podjetju: Mapped[datetime.date]
    leta_delovne_dobe: Mapped[int]
    tedenska_delovna_obveznost: Mapped[int]

    def name_get(self):
        return self.delojemalec

    def id_get(self):
        return self.id


class KategorijaIzplacila(Base):
    __tablename__ = 'kategorija_izplacila'
    id: Mapped[int] = mapped_column(primary_key=True)
    oznaka: Mapped[str] = mapped_column(String(12))
    naziv: Mapped[str] = mapped_column(String(50))
    vrste_izplacil: Mapped[list["VrstaIzplacila"]] = relationship(back_populates="kategorija",
                                                                  cascade="all, delete-orphan")

    def name_get(self):
        return f"{self.oznaka} {self.naziv}"

    def id_get(self):
        return self.id


class VrstaIzplacila(Base):
    __tablename__ = 'vrsta_izplacila'
    id: Mapped[int] = mapped_column(primary_key=True)
    oznaka: Mapped[str] = mapped_column(String(12))
    naziv: Mapped[str] = mapped_column(String(50))
    formula: Mapped[str]
    kategorija_id: Mapped[int] = mapped_column(ForeignKey("kategorija_izplacila.id"),
                                               nullable=False)
    kategorija: Mapped["KategorijaIzplacila"] = relationship(back_populates="vrste_izplacil")
    pozicije_pl: Mapped[list["PlacilnaListaPozicija"]] = relationship(back_populates="vrsta_izplacila",
                                                                      cascade="all, delete-orphan")

    def name_get(self):
        return f"{self.oznaka} {self.naziv}"

    def id_get(self):
        return self.id


class PlacilnaLista(Base):
    __tablename__ = 'placilna_lista'
    id: Mapped[int] = mapped_column(primary_key=True)
    sklic: Mapped[str] = mapped_column(String(10))
    delojemalec_id: Mapped[int] = mapped_column(ForeignKey("delojemalec.id"), nullable=False)
    delojemalec: Mapped["Delojemalec"] = relationship(back_populates="placilne_liste")
    datum_obracuna_od: Mapped[str] = mapped_column(String(10))
    datum_obracuna_do: Mapped[str] = mapped_column(String(10))
    datum_izplacila: Mapped[str] = mapped_column(String(10))
    pozicije: Mapped[list["PlacilnaListaPozicija"]] = relationship(back_populates='placilna_lista',
                                                                   cascade="all, delete-orphan")

    def name_get(self):
        return f"{self.sklic} {self.delojemalec.priimek} {self.delojemalec.ime}"

    def id_get(self):
        return self.id


class PlacilnaListaPozicija(Base):
    __tablename__ = 'placilna_lista_pozicija'
    id: Mapped[int] = mapped_column(primary_key=True)
    placilna_lista_id: Mapped[int] = mapped_column(ForeignKey('placilna_lista.id'))
    placilna_lista: Mapped["PlacilnaLista"] = relationship(back_populates='pozicije')
    vrsta_izplacila_id: Mapped[int] = mapped_column(ForeignKey("vrsta_izplacila.id"))
    vrsta_izplacila: Mapped["VrstaIzplacila"] = relationship(back_populates="pozicije_pl")
    kolicina: Mapped[float]
    vrednost_na_enoto: Mapped[float]
    osnova: Mapped[float]
    odstotek: Mapped[float]
    skupaj: Mapped[float]

    FIELDS_HEADERS = [
        ('vrsta_izplacila.naziv', 'Vrsta izplačila'),
        ('kolicina', 'Količina'),
        ('vrednost_na_enoto', 'Vrednost na em.'),
        ('osnova', "Osnova"),
        ('odstotek', "Odstotek"),
        ('skupaj', "Skupaj"),
    ]

    def name_get(self):
        return f"{self.placilna_lista.sklic} {self.vrsta_izplacila.naziv}"

    def id_get(self):
        return self.id


if __name__ == '__main__':
    # Base.metadata.create_all(engine)
    # lucija = session.get(Delojemalec, 7)
    # print(lucija.ime)
    # lucija.otroci.append(Otrok(ime="Domen"))
    # session.commit()
    pl = session.get(PlacilnaLista, 1)
    print(pl.sklic)
    # pl.pozicije.append(PlacilnaListaPozicija(vrsta_izplacila_id=1, kolicina=1,
    #                                          vrednost_na_enoto=1,
    #                                          osnova=1,
    #                                          odstotek=100,
    #                                          skupaj=1))
    session.commit()
    session.close()
    # stmt = select(Delojemalec)
    # name = "Lucija"
    # stmt = stmt.where(Delojemalec.id == bindparam('id'))
    # result =  session.scalars(stmt, {'id': 11}).all()
    # print(result[0].ime, result[0].priimek, len(result))
