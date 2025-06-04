
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+asyncpg://postgres:Oceanportal2017*@localhost/library_db"

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Async session factory
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Base model
Base = declarative_base()
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Use environment variable for database URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:Oceanportal2017*@localhost/library_db")

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Async session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base model
Base = declarative_base()
