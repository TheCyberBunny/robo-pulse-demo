"""
Day 3 - creates every table and enum type defined by the SQLAlchemy
models, via Base.metadata.create_all through the async engine.

Run from backend/ with the venv active:
    python -m scripts.day3_create_tables
"""

import asyncio

from app.database import engine
from app.models import Base


async def create_tables() -> None:
    async with engine.begin() as conn:
        #create_all() is a method provided by SQLAlchemy's MetaData object that
        #creates all tables defined in the metadata.
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(create_tables())