from pydantic import BaseModel
from pydantic.fields import Field

'''
This schema will be used for validatig the payloads
used to create and update notes
'''
class NoteSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)

class NoteDB(NoteSchema):
    id: int
