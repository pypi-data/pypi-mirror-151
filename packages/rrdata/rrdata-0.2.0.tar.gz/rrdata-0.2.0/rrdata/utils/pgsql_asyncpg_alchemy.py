from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import select

from rrdata.utils.rqSetting import setting
from rrdata.utils.rqLogs import rq_util_log_info

passwd_postgres = setting["PGSQL_PASSWORD"]
host_ip = setting["IP_DATABASE_ALIYUN"]
db_name = setting["DATABASE"]
table_name = "cities"

DATABASE_URL = f"postgresql+asyncpg://postgres:{passwd_postgres}@{host_ip}:5432/{db_name}"

engine = create_async_engine(DATABASE_URL, echo=True)
rq_util_log_info(engine)
#Base class
Base = declarative_base()
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
rq_util_log_info(async_session)


class City(Base):
    __tablename__ = table_name

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, unique=True)
    population = Column(Integer)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# Dependency
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def get_biggest_cities(session: AsyncSession) -> list[City]:
    result = await session.execute(select(City).order_by(City.population.desc()).limit(20))
    return result.scalars().all()


def add_city(session: AsyncSession, name: str, population: int):
    new_city = City(name=name, population=population)
    rq_util_log_info(f" add new_city: name: {name}, population: {population}")
    session.add(new_city)
    return new_city


if  __name__ == '':
    #get_biggest_cities()
    add_city(get_session(),"shenzhen",1700)