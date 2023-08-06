import logging
import pstats
from symtable import Symbol
import pandas as pd

from rrdata.utils.rqCode import rq_util_str_tounitecode
from rrdata.utils.rqLogs import rq_util_log_debug, rq_util_log_info, rq_util_log_expection
from rrdata.rrdatad.stock import stock_zh_a_hist_em, stock_zh_a_spot_em
from rrdata.common import save_df_to_pgsql, read_df_from_table


startDate = "20220501"
def get_stock_daily_one(symbol="600519",period="daily",start_date=startDate, end_date="20321231", adjust="hfq"):
    """ 
    hist daily from eastmoney
    adjust: : "hfq"
    #HowTO get stock adhust_factor
    """
    df = stock_zh_a_hist_em(symbol,period,start_date,end_date,adjust)
    df['ts_code'] = rq_util_str_tounitecode(symbol)
    df = df[['ts_code','trade_date','open','high','low','close','chg_pct','vol','amount']]
    return df

def save_stock_daily(stock_list=None,db_name='stock_day'):
    """TODO  use asyncio -- postgres+asyncpg://host/dbname --engine
        5000 class to 20 class 250 unit
    """
    lists = read_df_from_table('stock_list').symbol.values if None else stock_list
    rq_util_log_debug(lists)
    for symbol in lists:
        try:
            data = get_stock_daily_one(symbol)
            save_df_to_pgsql(data,db_name,if_exists='append')
        except Exception as e:
            rq_util_log_expection(e)
            
   

if  __name__ == "__main__":
    list1 = ['600519','000792','835185']
    save_stock_daily(list1, 'stock_day_test')
   
    read_df_from_table('stock_day_test')
   


