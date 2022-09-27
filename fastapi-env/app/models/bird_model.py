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

    def __init__(self,id, name, short, image, recon, food, see, uuid = generate_uuid()):
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

    uuid = Column(String(36))
    id = Column(String(36), primary_key=True)
    name = Column(String(36))
    short = Column(String(1000))
    image = Column(String(1000))
    recon = Column(TextPickleType)
    food = Column(TextPickleType)
    see = Column(String(1000))

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