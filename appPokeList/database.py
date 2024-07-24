from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from .config import settings

engine = create_async_engine(
    settings.database_url, connect_args={"check_same_thread": False}
)
async_session = sessionmaker(
	autocommit=False,
	autoflush=False,
	bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session