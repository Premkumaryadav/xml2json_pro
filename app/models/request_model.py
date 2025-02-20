from pydantic import BaseModel

class RequestModel(BaseModel):
    xml_data: str
