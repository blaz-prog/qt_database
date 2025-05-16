from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import URL

url_object = URL.create(
    drivername='postgresql+psycopg2',
    username='blaz',
    password='buratino',
    host='localhost',
    database='kadri'
)
engine = create_engine(url_object)
session = Session(engine)
