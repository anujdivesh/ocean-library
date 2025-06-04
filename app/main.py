import sys
from pathlib import Path

# Add /app to Python path (since Docker copies files to /app)
sys.path.append(str(Path(__file__).parent))
from typing import Union
from fastapi import FastAPI, Request, Response, APIRouter, Depends, HTTPException, Header, status, UploadFile, File, Form, Query
from fastapi.responses import JSONResponse, StreamingResponse,FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import io, os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.db import AsyncSessionLocal
from app.models import Country
from sqlalchemy import select
from app.schemas import CountryCreate, YearCreate, DocumentTypeCreate
from sqlalchemy.orm import selectinload
import os
import shutil
from uuid import uuid4
from app.models import DocumentType, Year, Document
from app.schemas import DocumentTypeCreate,  DocumentTypeOut, YearOut, DocumentOut
from typing import List, Optional
from sqlalchemy import asc, desc

API_TOKEN = "99a920305541f1c38db611ebab95ba"

#UPLOAD_DIR = "app/uploads/documents"



async def verify_token(x_token: str = Header(...)):
    if x_token != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token"
        )


app = FastAPI(
    docs_url="/library/docs",
    redoc_url="/library/redoc",
    openapi_url="/library/openapi.json",
    favicon_url="/library/favicon.ico"
)
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# .

# Dependency
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

ocean_router = APIRouter(prefix="/library")
UPLOAD_DIR = Path(__file__).parent.parent / "app" / "uploads" / "documents"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Mount static files
ocean_router.mount(
    "/media",
    StaticFiles(directory=str(UPLOAD_DIR.absolute())),  # Must be absolute path
    name="media"
)


@ocean_router.get("/")
def read_root():
    return {"Message": "Welcome to Ocean Portal Library, powered by OpenAPI"}

# Favicon route (must include the prefix)
@app.get("/favicon.ico", include_in_schema=False)
@ocean_router.get("/favicon.ico", include_in_schema=False)
async def get_favicon():
    # Get the absolute path to the favicon
    favicon_path = Path(__file__).parent / "icon.ico"
    if not favicon_path.exists():
        raise HTTPException(status_code=404, detail="Favicon not found")
    return FileResponse(favicon_path)


####COUNTRY FUNCTIONS
@ocean_router.get("/countries/")
async def read_countries(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Country).order_by(asc(Country.value)))
    countries = result.scalars().all()
    return countries

@ocean_router.post("/countries/", dependencies=[Depends(verify_token)])
async def create_country(country: CountryCreate,db: AsyncSession = Depends(get_db)):
    new_country = Country(value=country.value, name=country.name)
    db.add(new_country)
    try:
        await db.commit()
        await db.refresh(new_country)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Country already exists or DB error")
    return new_country

@ocean_router.delete("/countries/{country_id}", dependencies=[Depends(verify_token)])
async def delete_country(country_id: int,db: AsyncSession = Depends(get_db)):
    # First check if the country exists
    result = await db.execute(select(Country).where(Country.id == country_id))
    country = result.scalar_one_or_none()
    
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    
    try:
        await db.delete(country)
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Cannot delete country due to existing references or other constraints"
        )
    
    return {"message": f"Country with ID {country_id} deleted successfully"}

##DOCUMENT TYPES
@ocean_router.get("/document-types/", response_model=List[DocumentTypeOut])
async def get_document_types(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DocumentType))
    return result.scalars().all()

@ocean_router.post("/document-types/", dependencies=[Depends(verify_token)])
async def create_document_type(doc: DocumentTypeCreate,db: AsyncSession = Depends(get_db)):
    new_doc = DocumentType(value=doc.value, name=doc.name)
    db.add(new_doc)
    try:
        await db.commit()
        await db.refresh(new_doc)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Document type already exists")
    return new_doc

@ocean_router.delete("/document-types/{doc_type_id}", dependencies=[Depends(verify_token)])
async def delete_document_type(doc_type_id: int,db: AsyncSession = Depends(get_db)):
    # Check if document type exists
    result = await db.execute(
        select(DocumentType).where(DocumentType.id == doc_type_id)
    )
    doc_type = result.scalar_one_or_none()
    
    if not doc_type:
        raise HTTPException(
            status_code=404,
            detail="Document type not found"
        )
    
    try:
        await db.delete(doc_type)
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Cannot delete document type - it may be in use by existing documents"
        )
    
    return {
        "message": f"Document type with ID {doc_type_id} deleted successfully",
        "deleted_value": doc_type.value,
        "deleted_name": doc_type.name
    }

##YEARS
@ocean_router.get("/years/", response_model=List[YearOut])
async def get_years(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Year).order_by(desc(Year.value)))
    return result.scalars().all()

@ocean_router.post("/years/", dependencies=[Depends(verify_token)])
async def create_year(year: YearCreate, db: AsyncSession = Depends(get_db)):
    new_year = Year(value=year.value, name=year.name)
    db.add(new_year)
    try:
        await db.commit()
        await db.refresh(new_year)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Year already exists")
    return new_year

@ocean_router.delete("/years/{year_id}", dependencies=[Depends(verify_token)])
async def delete_year(year_id: int,db: AsyncSession = Depends(get_db)):
    # Check if year exists
    result = await db.execute(
        select(Year).where(Year.id == year_id)
    )
    year = result.scalar_one_or_none()
    
    if not year:
        raise HTTPException(
            status_code=404,
            detail="Year not found"
        )
    
    try:
        await db.delete(year)
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Cannot delete year - it may be referenced by other records"
        )
    
    return {
        "message": f"Year with ID {year_id} deleted successfully",
        "deleted_value": year.value,
        "deleted_name": year.name
    }

#DOCUMENTS
@ocean_router.get("/documents/", response_model=List[DocumentOut])
async def get_documents(
    country_id: Optional[int] = Query(None, description="Filter by country ID"),
    document_type_id: Optional[int] = Query(None, description="Filter by document type ID"),
    year_id: Optional[int] = Query(None, description="Filter by year ID"),
    db: AsyncSession = Depends(get_db)
):
    # Start building the query with explicit joins
    query = (
        select(Document)
        .join(Document.year)  # Explicitly join Year table
        .join(Document.country)  # Join Country table for sorting
        .options(
            selectinload(Document.country),
            selectinload(Document.document_type),
            selectinload(Document.year)
        )
    )
    
    # Apply filters
    if country_id is not None:
        query = query.where(Document.country_id == country_id)
    if document_type_id is not None:
        query = query.where(Document.document_type_id == document_type_id)
    if year_id is not None:
        query = query.where(Document.year_id == year_id)
    
    # Correct sorting using the joined Year model
    query = query.order_by(
        desc(Year.value),  # Sort by year descending (newest first)
        asc(Country.name)   # Then by country name ascending
    )
    
    # Execute query
    result = await db.execute(query)
    documents = result.unique().scalars().all()
    
    return documents

@ocean_router.post("/documents/", response_model=DocumentOut, dependencies=[Depends(verify_token)])
async def create_document(title: str = Form(...),country_id: int = Form(...),document_type_id: int = Form(...),year_id: int = Form(...),image: UploadFile = File(...),pdf: UploadFile = File(...),db: AsyncSession = Depends(get_db)):
    # Validate file types
    if not image.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise HTTPException(400, "Image must be PNG or JPG")
    
    if not pdf.filename.lower().endswith('.pdf'):
        raise HTTPException(400, "PDF file required")

    try:
        # Generate unique filenames
        image_ext = Path(image.filename).suffix
        pdf_ext = Path(pdf.filename).suffix
        
        image_filename = f"{uuid4().hex}_img{image_ext}"
        pdf_filename = f"{uuid4().hex}_pdf{pdf_ext}"

        # Save files
        image_path = UPLOAD_DIR / image_filename
        pdf_path = UPLOAD_DIR / pdf_filename

        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        with open(pdf_path, "wb") as buffer:
            shutil.copyfileobj(pdf.file, buffer)

        # Create document with just filenames
        new_doc = Document(
            title=title,
            country_id=country_id,
            document_type_id=document_type_id,
            year_id=year_id,
            image=image_filename,
            pdf=pdf_filename
        )

        db.add(new_doc)
        await db.commit()
        
        # Eager load all relationships for the response
        result = await db.execute(
            select(Document)
            .where(Document.id == new_doc.id)
            .options(
                selectinload(Document.country),
                selectinload(Document.document_type),
                selectinload(Document.year)
            )
        )
        document = result.scalar_one()
        
        return document

    except Exception as e:
        # Clean up any files that might have been created
        for filepath in [image_path, pdf_path]:
            if 'filepath' in locals() and filepath and filepath.exists():
                try:
                    filepath.unlink()
                except:
                    pass
        
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload document: {str(e)}"
        )

@ocean_router.delete("/documents/{document_id}", dependencies=[Depends(verify_token)])
async def delete_document(document_id: int, db: AsyncSession = Depends(get_db)):
    # Check if document exists
    result = await db.execute(
        select(Document).where(Document.id == document_id)
    )
    document = result.scalar_one_or_none()
    
    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )
    
    # Store file paths before deletion
    image_path = UPLOAD_DIR / document.image
    pdf_path = UPLOAD_DIR / document.pdf
    
    try:
        # Delete database record
        await db.delete(document)
        await db.commit()
        
        # Delete associated files
        try:
            if image_path.exists():
                os.unlink(image_path)
            if pdf_path.exists():
                os.unlink(pdf_path)
        except OSError as e:
            print(f"⚠️ Warning: Could not delete files for document {document_id}: {e}")
            # We continue even if file deletion fails
            
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Cannot delete document - it may be referenced by other records"
        )
    
    return {
        "message": f"Document with ID {document_id} deleted successfully",
        "deleted_title": document.title,
        "deleted_id": document.id
    }

@ocean_router.get("/media/{filename}")
async def get_media_file(filename: str):
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)
# Include the router
app.include_router(ocean_router)
