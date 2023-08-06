#!/usr/bin/python
""" see bigquant doc
    DataSource("basic_info_IndustrySw").read(instruments=stock_lists)
    out: DataFrame
"""

from http import client
from rrdata.common import save_df_to_pgsql
from rrdata.common.engine_pgsql import engine
from sqlalchemy import table


class RrdataDSave(object):
    """ see:
        bigquant DataSource("trade_days").read() 
        also add  can change:
        save data(dataframe) to database-table by sql_driver
    """
    def __init__(self, table_name, 
               database=engine(driver="", db_name="rrdata"),
                ):
        """ driver: ""-default - poasgresql/ psycopg2   db_name  rrdata/rrshare/rrfactor"""
        self.table_name = table_name
        self.engine = database

    def __repr__(self) -> str:  # name 
        return f"<{self.__class__.__name__} table_name={self.table_name}>"

    #def read(self):  # read artubuite
    #    return  read_df_from_table(self.table_name, self.engine)

    def save(self, data):
        #print(f"----save data to {self.table_name}")
        return save_df_to_pgsql(data, self.table_name)


if  __name__ == "__main__":
    #from rrdata.rrdatad.stock.fetch_stock_list import  fetch_stock_list_tusharepro
    #data = fetch_stock_list_tusharepro()
    #table_name = 'stock_list_tspro'
    #print(RrdataDSave(table_name).__repr__())
    #RrdataDSave(table_name).save(data)
    from rrdata.rrdatad.stock.stock_zh_a_hist_em import stock_zh_a_spot_em
    RrdataDSave("stock_spot_20220516").save(stock_zh_a_spot_em())
    



