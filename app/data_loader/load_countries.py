# load.py
import asyncio
import json
from app.db import AsyncSessionLocal, engine
from app.models import Country
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

async def load_countries_from_json():
    with open("app/data_loader/countries.json", "r") as f:
        data = json.load(f)

    async with AsyncSessionLocal() as session:
        for item in data["countries_list"]:
            country = Country(value=item["value"], name=item["name"])
            session.add(country)
        try:
            await session.commit()
            print("✅ Countries inserted successfully")
        except IntegrityError as e:
            await session.rollback()
            print(f"⚠️  Integrity error: {e}")

if __name__ == "__main__":
    asyncio.run(load_countries_from_json())
