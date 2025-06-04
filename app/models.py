from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class Country(Base):
    __tablename__ = "countries"
    __table_args__ = {'extend_existing': True}  # Correct placement
    
    id = Column(Integer, primary_key=True, index=True)
    value = Column(String, index=True)
    name = Column(String, index=True)


class DocumentType(Base):
    __tablename__ = "document_types"
    __table_args__ = {'extend_existing': True}  # Add for consistency
    
    id = Column(Integer, primary_key=True, index=True)
    value = Column(String, unique=True, index=True)
    name = Column(String, index=True)


class Year(Base):
    __tablename__ = "years"
    __table_args__ = {'extend_existing': True}  # Add for consistency

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Integer, unique=True, index=True)
    name = Column(Integer, index=True)


class Document(Base):
    __tablename__ = "documents"
    __table_args__ = {'extend_existing': True}  # Add for consistency

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    country_id = Column(Integer, ForeignKey("countries.id"))
    document_type_id = Column(Integer, ForeignKey("document_types.id"))
    year_id = Column(Integer, ForeignKey("years.id"))
    image = Column(String)
    pdf = Column(String)

    # Relationships
    country = relationship("app.models.Country", backref="documents")
    document_type = relationship("app.models.DocumentType", backref="documents")
    year = relationship("app.models.Year", backref="documents")