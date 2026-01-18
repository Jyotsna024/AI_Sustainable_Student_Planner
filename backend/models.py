from pydantic import BaseModel

class StudentInput(BaseModel):
    sleep:int
    screen:int
    study:int
    travel:str
