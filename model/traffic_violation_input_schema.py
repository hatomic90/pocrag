from pydantic import BaseModel


class UserInputSchema(BaseModel):
    text: str
