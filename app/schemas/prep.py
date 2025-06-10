from pydantic import BaseModel

class PrepFullRequest(BaseModel):
    client_id: str

class PrepFullResponse(BaseModel):
    prep_id: str
