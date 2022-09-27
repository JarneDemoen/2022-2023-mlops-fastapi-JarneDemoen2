from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    uuid: Optional[str]
    id: str
    name: str
    locationOfResidence: str
    age: int
    gender: str
    registrationDate: str

    class Config:
        orm_mode = True

    def sayHello(self):
        return f"Hello User {self.name}!"
