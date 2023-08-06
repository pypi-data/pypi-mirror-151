# coding:utf-8
import asyncio
import asyncpg
import psycopg2

from rrdata.utils.config_setting import setting


host = setting['IP_DATABASE_ALIYUN']
db_name = setting["DATABASE"]
passwd = setting["PGSQL_PASSWORD"]
uri = f'postgresql://postgres:{passwd}@{host}:5432/{db_name}'

# connect client
def rq_util_sql_postgres_setting(uri=uri):
    # 使用uri代替ip,port的连接方式
    # 这样可以对postgresql进行加密:
    # uri=postgresql://user:passwor@ip:port/daatbase
    client = psycopg2.connect(uri)
    #print(client)
    return client


# async
def rq_util_sql_async_postgres_setting(uri=uri):  #TODO
    #loop = asyncio.new_event_loop()
    #asyncio.set_event_loop(loop)
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    # async def client():
    return loop
    #return loop.run_until_complete(uri)
    # yield  client()

##ASCENDING = psycopg2.ASCENDING
##DESCENDING = psycopg2.DESCENDING
#rq_util_sql_postgres_sort_ASCENDING = psycopg2.ASCENDING
#rq_util_sql_postgres_sort_DESCENDING = psycopg2.DESCENDING

if __name__ == '__main__':
    # test client
    print(rq_util_sql_postgres_setting())
    # test async_postgres
    client = rq_util_sql_async_postgres_setting()
    #client.rrdata.swl_list
    #print(client)

