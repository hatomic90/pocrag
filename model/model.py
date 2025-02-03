from pydantic import BaseModel

# Melhor referenciar a esse modulo como Schema
class UserInput(BaseModel):
    text: str
