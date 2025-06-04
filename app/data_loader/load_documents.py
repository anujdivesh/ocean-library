import json
import asyncio
import os
import aiohttp
from uuid import uuid4
from sqlalchemy.future import select
from app.db import AsyncSessionLocal
from app.models import Country, DocumentType, Year, Document
from pathlib import Path

# Configure upload directory
UPLOAD_DIR = Path("app/uploads/documents")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

async def download_file(session, url, suffix):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                ext = url.split(".")[-1].split("?")[0]  # handle .png?key=abc
                filename = f"{uuid4().hex}_{suffix}.{ext}"
                filepath = UPLOAD_DIR / filename
                
                # Save file
                with open(filepath, "wb") as f:
                    f.write(await response.read())
                
                # Return only the filename, not full path
                return filename
            else:
                print(f"⚠️ Failed to download {url} — HTTP {response.status}")
    except Exception as e:
        print(f"⚠️ Error downloading {url}: {e}")
    return None

async def load_documents():
    async with AsyncSessionLocal() as db, aiohttp.ClientSession() as session:
        with open("app/data_loader/documents.json") as f:
            data = json.load(f)

        for entry in data["documents"]:
            title = entry["title"]
            country_value = entry["category"]
            doc_type_value = entry["document"]
            year_value = entry["year"]  # This comes as string from JSON
            image_url = entry["image"]
            pdf_url = entry["pdf"]

            # Convert year string to integer
            try:
                year_int = int(year_value)
            except (ValueError, TypeError):
                print(f"⚠️ Invalid year format: {year_value}")
                continue

            # Resolve FKs
            country = await db.execute(select(Country).where(Country.value == country_value))
            country_obj = country.scalar_one_or_none()
            if not country_obj:
                print(f"⚠️ Country not found: {country_value}")
                continue

            doc_type = await db.execute(select(DocumentType).where(DocumentType.value == doc_type_value))
            doc_type_obj = doc_type.scalar_one_or_none()
            if not doc_type_obj:
                print(f"⚠️ Document Type not found: {doc_type_value}")
                continue

            year = await db.execute(select(Year).where(Year.value == year_int))  # Now using integer
            year_obj = year.scalar_one_or_none()
            if not year_obj:
                print(f"⚠️ Year not found: {year_int}")
                continue

            # Download files (returns just filenames now)
            image_filename = await download_file(session, image_url, "img")
            pdf_filename = await download_file(session, pdf_url, "pdf")

            if not image_filename or not pdf_filename:
                print(f"⚠️ Skipping {title} due to missing files.")
                continue

            # Save document with just filenames
            doc = Document(
                title=title,
                country_id=country_obj.id,
                document_type_id=doc_type_obj.id,
                year_id=year_obj.id,
                image=image_filename,  # Just the filename
                pdf=pdf_filename      # Just the filename
            )

            db.add(doc)

        await db.commit()
        print("✅ All documents processed.")

if __name__ == "__main__":
    asyncio.run(load_documents())