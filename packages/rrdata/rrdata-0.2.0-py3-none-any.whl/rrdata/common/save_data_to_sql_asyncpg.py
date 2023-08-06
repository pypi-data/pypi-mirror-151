import asyncio
import asyncpg
import json
import datetime

from rrdata.common.engine_pgsql import database_dns, engine


async def main(db_name='rrdata'):
    conn = await asyncpg.connect(f"{database_dns}/{db_name}")

    try:
        await conn.set_type_codec(
            'json',
            encoder=json.dumps,
            decoder=json.loads,
            schema='pg_catalog'
        )

        data = {'foo': 'bar', 'spam': 1}
        res = await conn.fetchval('SELECT $1::json', data)

    finally:
        await conn.close()

async def main2(db_name='rrdata'):
    # Establish a connection to an existing database named "test"
    # as a "postgres" user.
    conn = await asyncpg.connect(f"{database_dns}/{db_name}")
    # Execute a statement to create a new table.
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id serial PRIMARY KEY,
            name text,
            dob date
        )
    ''')

    # Insert a record into the created table.
    await conn.execute('''
        INSERT INTO users(name, dob) VALUES($1, $2)
    ''', 'Bob', datetime.date(1984, 3, 1))

    # Select a row from the table.
    row = await conn.fetchrow(
        'SELECT * FROM users WHERE name = $1', 'Bob')
    # *row* now contains
    print(row)
    #asyncpg.Record(id=1, name='Bob', dob=datetime.date(1984, 3, 1))

    # Close the connection.
    await conn.close()

if  __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
    from rrdata.common import read_df_from_table
    #print(read_df_from_table('swl_list',engine()))
    #asyncio.get_event_loop().run_until_complete(main2())
    #print(read_df_from_table("users"))