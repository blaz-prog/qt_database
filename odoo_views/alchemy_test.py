from generic_mvc_alchemy.generic_table_model import GenericTableModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from postgresql_engine.engine import engine, session
from app_models.app_tables import Delojemalec


if __name__ == '__main__':

    print("Zacnimo testirati")
    with Session(engine) as test_session:
        stmt = select(Delojemalec).order_by('id')
        vsi_delojemalci  = test_session.scalars(stmt).all()
        print(type(vsi_delojemalci[1]))
    for i, delojemalec in enumerate(vsi_delojemalci):
        print(delojemalec)

    prvi = vsi_delojemalci[1]
    print("Priimek prvega je ", prvi.priimek)
    print("Spremenil sem priimek")
    prvi.priimek = "Strmčnik"
    print("Priimek prvega je ", prvi.priimek)

    print("============================================")
    print("Po spremembi priimka")
    print("============================================")
    with Session(engine) as update_session:
        update_session.add(prvi)
        update_session.commit()

    with Session(engine) as test_session:
        stmt = select(Delojemalec).order_by("id")
        vsi_delojemalci  = test_session.scalars(stmt).all()

    for i, delojemalec in enumerate(vsi_delojemalci):
        print(delojemalec)
