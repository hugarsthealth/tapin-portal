from sqlalchemy import Table, Column, Integer, String, ForeignKey

from models import Base

patient_role_table = Table('patient_role_association', Base.metadata,
    Column('patient_nhi', String(10), ForeignKey('patient.nhi')),
    Column('role_id', Integer, ForeignKey('role.role_id')),
)
