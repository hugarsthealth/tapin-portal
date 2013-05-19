from sqlalchemy import Table, Column, Integer, String, ForeignKey

from models import Base

patient_department_table = Table('patient_department_association', Base.metadata,
    Column('patient_nhi', String(10), ForeignKey('patient.nhi')),
    Column('department_id', Integer, ForeignKey('department.department_id')),
)
