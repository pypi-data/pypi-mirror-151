from rrdata.rrdatad.stock.fetch_stock_list import fetch_stock_list_tusharepro
from rrdata.common import save_df_to_pgsql
from rrdata.rrdatad.stock.stock_zh_a_hist_em import stock_zh_a_spot_em

save_df_to_pgsql(fetch_stock_list_tusharepro(), 'stock_list')

#stock_spot = stock_zh_a_spot_em()

save_df_to_pgsql(stock_zh_a_spot_em(), 'stock_spot')


