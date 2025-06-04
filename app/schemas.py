from pydantic import BaseModel,validator
from typing import Optional


# ---------- COUNTRY ----------
class CountryCreate(BaseModel):
    value: str
    name: str


class CountryOut(CountryCreate):
    id: int

    class Config:
        orm_mode = True


# ---------- DOCUMENT TYPE ----------
class DocumentTypeCreate(BaseModel):
    value: str
    name: str


class DocumentTypeOut(DocumentTypeCreate):
    id: int

    class Config:
        orm_mode = True


# ---------- YEAR ----------
class YearCreate(BaseModel):
    value: int
    name: int


class YearOut(YearCreate):
    id: int

    class Config:
        orm_mode = True


# ---------- DOCUMENT ----------
class DocumentCreate(BaseModel):
    title: str
    country_id: int
    document_type_id: int
    year_id: int


class DocumentOut(BaseModel):
    id: int
    title: str
    country: CountryOut
    document_type: DocumentTypeOut
    year: YearOut
    image: str
    pdf: str

    class Config:
        orm_mode = True

    @validator('image', 'pdf', pre=True)
    def convert_to_url(cls, value):
        if not value:
            return None
        # Extract just the filename if a full path was stored
        filename = value.split('/')[-1] if '/' in value else value
        return f"/library/media/{filename}"