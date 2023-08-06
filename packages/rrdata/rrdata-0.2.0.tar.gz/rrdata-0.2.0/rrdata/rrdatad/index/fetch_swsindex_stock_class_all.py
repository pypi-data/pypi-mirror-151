from rrdata.common import save_df_to_pgsql

import pandas as pd
file = "/home/romep/rrdata/rrdata/rrdatad/index/stock_swindex_class_all.csv"

path_file = u"/home/romep/rrdata/rrdata/rrdatad/index/swsindex/swsindex_all_stock_class_new.xlsx"

df = pd.read_excel(path_file)

save_df_to_pgsql(df, "swl_stock_class_all_2021_cn")
print(df)

print(df.columns)




