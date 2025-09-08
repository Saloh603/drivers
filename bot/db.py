from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@db:5432/rides")

# Create engine
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Session factory
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Init DB
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
