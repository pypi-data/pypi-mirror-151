from dataclasses import replace
from functools import reduce
from heapq import merge
from numpy import NaN
import pandas as pd 
from rrdata.common import save_df_to_pgsql, engine
import rrdata.rrdatad.index  as index
from rrdata.utils.rqLogs import rq_util_log_info
from rrdata.utils.rqParameter import SWL_LEVEL


def save_index_sw_class_pgsql(table_name='swl_list'):
    data = index.sw_index_class_all()
    #print(data)
    save_df_to_pgsql(data, table_name, engine)
    #print(read_data_from_pg("swl_list"))


def save_index_sw_spot(table_name="swl_spot", level =""):
    """ save swl index L1, L2 realtime price
    """
    for l in ["L1", "L2"]:
        data = index.sw_index_spot(l)
        save_df_to_pgsql(data, f"{table_name}_{l}", engine)


def  save_index_sw_cons_one_level(table_name='swl_cons',level=""):
    """
    for leve in SWL_LEVEL().LEVEL get all cons
    table_name = f"table_name_{level}"
    important: 
    drop_duplicates(subset=["stock_code"], keep='last', inplace=True)
    """
    dfs =[]
    for symbol in index.sw_index_class(level).index_code.values:
        rq_util_log_info(symbol)
        try:
            cons = index.sw_index_legulegu_cons(symbol)
            cons.replace("-", NaN, inplace=True)
            cons.dropna(how='all', axis=1, inplace=True)
            #cons.sort_values(by=['stock_code', 'in_time'], ascending=[True, True], inplace=True)
            #cons.drop_duplicates(subset=['stock_code'], keep='first', inplace=True)
            rq_util_log_info(cons)
            dfs.append(cons)
            #rq_util_log_info(dfs)
        except:
            pass
    df = pd.concat(dfs)
    df.sort_values(by=['stock_code', 'in_time'], ascending=[True, True], inplace=True)
    df.drop_duplicates(subset=['stock_code'], keep='last', inplace=True)
    rq_util_log_info(df)
    save_df_to_pgsql(df, f'{table_name}_{level}', engine)


def save_swl_cons_all_level(table_name='swl_cons_all'):
    from rrdata.common import read_df_from_table
    from rrdata.utils.rqParameter import SWL_LEVEL
    def read_sw_index_cons_L(level=""):
        return read_df_from_table(f"swl_cons_{level}", con=engine)
    df_list =[]   
    for L in SWL_LEVEL().LEVEL:
        df_list.append(f"df{L[-1]}")
        df_list[-1] = read_sw_index_cons_L(level=L)
        df_list[-1].replace("-", NaN, inplace=True)
        #rq_util_log_info(df)
        df_list[-1].dropna(how='all', axis=1, inplace=True)
        df_list[-1].drop_duplicates(subset=["stock_code"], keep='last', inplace=True)
        df_list[-1].drop(['no', 'in_time'], axis=1, inplace=True)
        rq_util_log_info(df_list[-1])
       
    df_m = pd.merge(df_list[0], df_list[1],  how='outer')
    df = pd.merge(df_m, df_list[2], how='outer')
    rq_util_log_info(df)
    save_df_to_pgsql(df, 'swl_cons_all', con=engine)


if  __name__ == '__main__':
    save_index_sw_class_pgsql()
    save_index_sw_spot()
    for l in SWL_LEVEL().LEVEL:
        save_index_sw_cons_one_level('swl_cons', l)
        
    save_swl_cons_all_level()
    




