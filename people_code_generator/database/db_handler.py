"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from ..config import DB_TYPE, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from .models import Base, Person

class DatabaseHandler:
    def __init__(self):
        self.engine = None
        self.Session = None
        self._connect_to_db()
        
    def _connect_to_db(self):
        try:
            if DB_TYPE == 'sqlite':
                db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), DB_NAME)
                self.engine = create_engine(f'sqlite:///{db_path}')
            elif DB_TYPE == 'postgresql':
                self.engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
            elif DB_TYPE == 'mysql':
                self.engine = create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
            else:
                raise ValueError(f"Unsupported database type: {DB_TYPE}")
            
            # Create tables if they don't exist
            Base.metadata.create_all(self.engine)
            
            # Create session maker
            self.Session = sessionmaker(bind=self.engine)
            
        except SQLAlchemyError as e:
            print(f"Database connection error: {e}")
            raise
    
    def get_session(self):
        return self.Session()
    
    def get_all_people(self):
        session = self.get_session()
        try:
            return session.query(Person).all()
        except SQLAlchemyError as e:
            print(f"Error fetching people: {e}")
            return []
        finally:
            session.close()
    
    def get_person_by_id(self, person_id):
        session = self.get_session()
        try:
            return session.query(Person).filter(Person.id == person_id).first()
        except SQLAlchemyError as e:
            print(f"Error fetching person: {e}")
            return None
        finally:
            session.close()
            
    def get_person_by_code(self, code):
        session = self.get_session()
        try:
            return session.query(Person).filter(Person.unique_code == code).first()
        except SQLAlchemyError as e:
            print(f"Error fetching person by code: {e}")
            return None
        finally:
            session.close()
    
    def add_person(self, person_data):
        session = self.get_session()
        try:
            new_person = Person(**person_data)
            session.add(new_person)
            session.commit()
            return new_person
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error adding person: {e}")
            return None
        finally:
            session.close()
    
    def update_person_code(self, person_id, code):
        session = self.get_session()
        try:
            person = session.query(Person).filter(Person.id == person_id).first()
            if person:
                person.unique_code = code
                session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error updating person code: {e}")
            return False
        finally:
            session.close()
"""
