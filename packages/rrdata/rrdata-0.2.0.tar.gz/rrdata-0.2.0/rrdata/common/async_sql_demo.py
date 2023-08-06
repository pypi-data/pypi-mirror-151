import pandas as pd
import asyncio
from rrdata.common import engine, engine_async


async def read_sql_async(stmt, con):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, pd.read_sql, stmt, con)


async def engine_async(db_name='rrdata'):
    engine = create_async_engine(
        "postgresql+asyncpg://postgres:{passwd}@{host}:5432/{db_name}", echo=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(meta.drop_all)
        await conn.run_sync(meta.create_all)

        await conn.execute(
            t1.insert(), [{"name": "some name 1"}, {"name": "some name 2"}]
        )

    async with engine.connect() as conn:

        # select a Result, which will be delivered with buffered
        # results
        result = await conn.execute(select(t1).where(t1.c.name == "some name 1"))

        print(result.fetchall())

    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine.dispose()

asyncio.run(async_main())

if __name__ == '__main__':

    #loop = asyncio.get_event_loop()
    #df = loop.run_until_complete(main())
    #loop.close()
    """
    # Establish a connection to an existing database named "test"
    # as a "postgres" user.
    conn = await asyncpg.connect('postgresql://postgres@localhost/test')

    asyncio.get_event_loop().run_until_complete(main())
    """
    # tasks = await asyncio.gather(*tasks)
    #df = await read_sql_async('stock_list',engine('rrshare'))
    #print(df)