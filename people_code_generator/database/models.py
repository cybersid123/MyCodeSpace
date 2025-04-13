"""
from sqlalchemy import Column, Integer, String, Date, Boolean, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Person(Base):
    __tablename__ = 'people'
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    email = Column(String(100), unique=True)
    phone = Column(String(20))
    address = Column(String(255))
    unique_code = Column(String(50), unique=True)
    photo = Column(LargeBinary)
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<Person(id={self.id}, name='{self.first_name} {self.last_name}', code='{self.unique_code}')>"
"""
