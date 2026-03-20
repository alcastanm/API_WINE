
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()



# url =("postgresql+asyncpg://bdpostgress_user:CxZ0rkCUckTkNp0t5B0WQ7zSPBwj6ALl@dpg-d5tv89h4tr6s739kjul0-a.oregon-postgres.render.com/bdpostgress")

#esta conexion es para desplegar de forma local contra el front local
url =("postgresql+asyncpg://postgres:123@localhost:5432/wines")

engine = create_async_engine(
                            url,
                            echo=True,
                            future=True,
                            # isolation_level="SERIALIZABLE"
                            )

asyncLocalDbConn = sessionmaker(
    bind=engine,
    class_= AsyncSession,
    expire_on_commit=True
)


async def get_db():
    async with asyncLocalDbConn() as session:
        yield session
