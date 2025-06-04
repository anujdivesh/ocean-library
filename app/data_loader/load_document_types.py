# load_document_types.py
import asyncio
import json
from sqlalchemy.exc import IntegrityError
from app.db import AsyncSessionLocal
from app.models import DocumentType

async def load_document_types():
    with open("app/data_loader/document_types.json", "r") as f:
        data = json.load(f)

    async with AsyncSessionLocal() as session:
        for item in data["document_types"]:
            doc_type = DocumentType(value=item["value"], name=item["name"])
            session.add(doc_type)
        try:
            await session.commit()
            print("✅ Document types inserted successfully")
        except IntegrityError as e:
            await session.rollback()
            print(f"⚠️ Integrity error: {e}")

if __name__ == "__main__":
    asyncio.run(load_document_types())
