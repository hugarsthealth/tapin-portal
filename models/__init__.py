import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(os.getenv('DATABASE_URL', 'sqlite:///./test.db'), convert_unicode=True)
db = scoped_session(sessionmaker(autocommit=False,
                                 autoflush=False,
                                 bind=engine))
Base = declarative_base()
Base.query = db.query_property()

from models.patient import Patient
from models.vitalinfo import VitalInfo


def init_db(num_patients=5, min_vital_infos=2, max_vital_infos=10):
    from models.sampledata import populate_database

    Base.metadata.create_all(bind=engine)
    populate_database(num_patients, min_vital_infos, max_vital_infos)
