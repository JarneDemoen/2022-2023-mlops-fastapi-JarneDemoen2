import uuid
from database import Base
import json
import sqlalchemy
from sqlalchemy.types import TypeDecorator
from sqlalchemy import Column, String, Integer
from database import db
from schemas.bird import Bird as BirdSchema

SIZE = 5120

class TextPickleType(TypeDecorator):

    impl = sqlalchemy.Text(SIZE)

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value

class Bird(Base):

    def generate_uuid():
        return str(uuid.uuid4())

    def __init__(self,id=None, name=None, short=None, image=None, recon=None, food=None, see=None, uuid = None):
        self.uuid = uuid
        self.id = id
        self.name = name
        self.short = short
        self.image = image
        self.recon = recon
        self.food = food
        self.see = see

        self.model = Bird
        self.schema = BirdSchema
        
        
    __tablename__ = "birds"

    uuid = Column(String(36),default = generate_uuid())
    id = Column(String(36), primary_key=True)
    name = Column(String(36))
    short = Column(String(1000))
    image = Column(String(1000))
    recon = Column(TextPickleType)
    food = Column(TextPickleType)
    see = Column(String(1000))

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

    def create(self, obj: BirdSchema):
        try:
            # print(type(obj))
            # return
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

    def delete_bird(self, id):
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
    
    def update_bird(self, id, obj: BirdSchema):
        try:
            obj_in_db = self.get_by(id=id)
            if obj_in_db is not None:
                db.query(self.model).filter(self.model.id == id).update(obj.dict())
                db.commit()
                print(f"{self.model} has been updated in the database!")
                obj = self.schema.from_orm(obj_in_db)
            else:
                obj = None
                print(f"No {self.model} was found with id {id}!")

            return obj
        except Exception as e:
            print(f"Error while updating {self.model}.")
            print("Rolling back the database commit.")
            print(e)
            db.rollback()

    def get_bird_by_id(self, id):
        try:
            obj = self.get_by(id=id)
            if obj is not None:
                print(f"{self.model} has been found in the database!")
                obj = self.schema.from_orm(obj)
            else:
                obj = None
                print(f"No {self.model} was found with id {id}!")

            return obj
        except Exception as e:
            print(f"Error while getting {self.model} by id.")
            print(e)
            db.rollback()

    def get_many_birds_based_on_property(self, property, value):
        try:
            db_objects = db.query(self.model).filter(getattr(self.model, property) == value).all() # The actual query
            if db_objects:
                return db_objects
            else:
                print(f"No {self.model} was found!")
                return None
        except Exception as e:
            print(f"Error while getting all {self.model}s.")
            print(e)
            db.rollback()