from pydantic import BaseModel, field_validator

class Model(BaseModel):
    userId: int
    id: int
    title: str
    body: str

    @field_validator("userId", "id", "title", "body")
    def fields_are_not_empty(cls, value):
        if value == "" or value is None:
            raise ValueError("Field is empty")
        else:
            return value

class PutModel(BaseModel):
    id: int
    body: str

    @field_validator("id", "body")
    def fields_are_not_empty(cls, value):
        if value == "" or value is None:
            raise ValueError("Field is empty")
        else:
            return value
