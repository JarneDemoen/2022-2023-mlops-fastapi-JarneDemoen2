import uuid
from database import Base
import sqlalchemy
from sqlalchemy import Column, String, Integer
from database import db
from schemas.user import User as UserSchema


class User(Base):

    def generate_uuid():
        return str(uuid.uuid4())

    def __init__(self,id=None, name=None, locationOfResidence=None, age=None, gender=None, registrationDate=None, uuid=None):
        self.uuid = uuid
        self.id = id
        self.name = name
        self.locationOfResidence = locationOfResidence
        self.age = age
        self.gender = gender
        self.registrationDate = registrationDate

        self.model = User
        self.schema = UserSchema
        
    __tablename__ = "users"

    uuid = Column(String(36), default=generate_uuid())
    id = Column(String(36), primary_key=True)
    name = Column(String(36))
    locationOfResidence = Column(String(1000))
    age = Column(Integer)
    gender = Column(String(36))
    registrationDate = Column(String(36))

    def get_by(self, **kwargs):
        try:
            return db.query(self.model).filter_by(**kwargs).first()
        except Exception as e:
            print(f"Error while getting {self.model} by {kwargs}.")
            print(e)
            db.rollback()

    def get_all(self):
        try:
            db_objects = db.query(self.model).all() # The actual query
            if db_objects:
                return db_objects
            else:
                print(f"No {self.model} was found!")
                return None
        except Exception as e:
            print(f"Error while getting all {self.model}s.")
            print(e)
            db.rollback()

    def create(self, obj: UserSchema):
        try:
            obj_in_db = self.get_by(name=obj.name)
            if obj_in_db is None:
                print(f"No {self.model} was found with name {obj.name}!")

                new_obj = self.model(**obj.dict())
                db.add(new_obj)
                db.commit()

                print(f"{self.model} has been added to the database!")
                obj = self.schema.from_orm(new_obj)
            else:
                obj = None
                print(f"A {self.model} already exists.")

            return obj

        except Exception as e:
            print(f"Error while creating {self.model}.")
            print("Rolling back the database commit.")
            print(e)
            db.rollback()

    def delete_user(self, id):
        try:
            obj = self.get_by(id=id)
            if obj is not None:
                db.delete(obj)
                db.commit()
                print(f"{self.model} has been deleted from the database!")
                return True
            else:
                print(f"No {self.model} was found with id {id}!")
                return False
        except Exception as e:
            print(f"Error while deleting {self.model}.")
            print("Rolling back the database commit.")
            print(e)
            db.rollback()
            return False