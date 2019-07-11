import requests
import pandas as pd
import io

## in primary function:
# data.requsts.get(url).content
# getExcelFile(data, cols) # PV
# getExcelFile(data, cols) # Storage
# getExcelFile(data, cols) # Wind
# ...

def getExcelFile(data, cols, units, sheetname):
	sheet = pd.read_excel(io.BytesIO(data), sheetname='Monthly_Totals-States', skiprows=2, skip_footer=1, parse_cols=cols)
	sheet.rename(columns={'Year':'year', 'Month':'month', 'State':'state'}, inplace=True)
	fileyyyy = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation', 'Direct Connected'], var_name='sector', value_name='value')
	fileyyyy['units'] = units
	#fileyyyy['type'] = 'PV'
	#if(sheetname != 'Photovoltaic'):
	#	fileyyyy['type'] = 'NA'
	fileyyyy['nem'] = 'No'
	fileyyyy['sheet'] = sheetname
	#print(fileyyyy.head(), '\n\n')
	return fileyyyy

def get2018():
	url = 'https://www.eia.gov/electricity/data/eia861m/archive/xls/non_netmetering2018.xlsx'
	data = requests.get(url).content
	df_1 = getExcelFile(data, 'A:C,I:M', 'MW', 'Photovoltaic')
	df_2 = getExcelFile(data, 'A:C,O:S', 'MW', 'Storage')
	df_3 = getExcelFile(data, 'A:C,U:Y', 'MW', 'Wind')
	df_4 = getExcelFile(data, 'A:C,AA:AE', 'MW', 'Hydroelectric')
	df_5 = getExcelFile(data, 'A:C,AG:AK', 'MW', 'Fuel Cells')
	df_6 = getExcelFile(data, 'A:C,AM:AQ', 'MW', 'Internal Combustion')
	df_7 = getExcelFile(data, 'A:C,AS:AW', 'MW', 'Combustion Turbine')
	df_8 = getExcelFile(data, 'A:C,AY:BC', 'MW', 'Steam')
	df_9 = getExcelFile(data, 'A:C,BE:BI', 'MW', 'Other')
	df = pd.concat([df_1, df_2, df_3, df_4, df_5, df_6, df_7, df_8, df_9])
	#df.loc[:, 'value'] = [0 if isinstance(x, str) else x for x in df['value']]
	return df

if __name__ == '__main__':
	temp = get2018()
	print(temp.head())
