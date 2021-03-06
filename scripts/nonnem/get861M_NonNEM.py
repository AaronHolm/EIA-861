import pandas as pd

from get2017 import get2017
from get2018 import get2018
from get2019 import get2019
from processer import processer
from to_sql import to_sql

def get861M():
	df_2017 = get2017()
	df_2018 = get2018()
	df_2019 = get2019()
	#df_2011 = processer(df_2011)
	#df_2012 = processer(df_2012)
	#df_2013 = processer(df_2013)
	#df_2014 = processer(df_2014)
	#df_2015 = processer(df_2015)
	#df_2016 = processer(df_2016)
	#df_2017 = processer(df_2017)
	#df_2018 = processer(df_2018)

	df_combined = pd.concat([df_2017, df_2018, df_2019])
	print(df_combined.head())
	df = processer(df_combined)
	df_combined.loc[:, 'value'] = [pd.to_numeric(x, errors='coerce') if isinstance(x, str) else float(x) for x in df_combined['value']]
	if(df.empty):
		print("Error with dataframe. Listed as empty.")
	else:
		#df.to_excel('/mnt/c/Users/AHolm/SEIA/OneDrive - SEIA/codebin/datasources/SEIA_DB/Outputs/eia826_2019Q1_NonNEM_v1.xlsx')
		to_sql(df)
		print(df.head(), '\n', df.tail())
		print("Successfully updated table markets.eia_826_nonnem")
	return

if __name__ == '__main__':
	get861M()
