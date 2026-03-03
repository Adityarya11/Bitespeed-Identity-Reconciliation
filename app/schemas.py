from pydantic import BaseModel, Field
from typing import List, Optional


class IdentifyRequest(BaseModel):
    email: Optional[str] = None
    phoneNumber: Optional[str] = None

class ContactResponseDetail(BaseModel):
    primaryContactId: int
    emails: List[str]
    phoneNumbers: List[str]
    secondaryContactIds: List[int]

    class Config:
        populate_by_name = True

class IdentifyResponse(BaseModel):
    contact: ContactResponseDetail