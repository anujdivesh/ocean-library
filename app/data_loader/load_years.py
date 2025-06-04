# load_years.py
import asyncio
import json
from sqlalchemy.exc import IntegrityError
from app.db import AsyncSessionLocal
from app.models import Year

async def load_years():
    with open("app/data_loader/years.json", "r") as f:
        data = json.load(f)

    async with AsyncSessionLocal() as session:
        for item in data["years"]:
            year = Year(value=item["value"], name=item["name"])
            session.add(year)
        try:
            await session.commit()
            print("✅ Years inserted successfully")
        except IntegrityError as e:
            await session.rollback()
            print(f"⚠️ Integrity error: {e}")

if __name__ == "__main__":
    asyncio.run(load_years())
