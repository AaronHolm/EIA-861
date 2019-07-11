import requests
import io
import pandas as pd

def get2011():
	link = 'https://www.eia.gov/electricity/data/eia861m/archive/xls/f826netmetering2011.xls'
	data = requests.get(link).content
	
	std_columns = ['year', 'month', 'state', 'Residential', 'Commercial', 'Industrial', 'Transportation']
	
	cap = pd.read_excel(io.BytesIO(data), sheetname='Month_State', parse_cols='A:C,I:L')
	cap.columns = std_columns
	df_2011 = pd.melt(cap, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	df_2011.loc[:, 'sheet'] = 'Capacity'
	df_2011.loc[:, 'type'] = 'PV'
	df_2011.loc[:, 'units'] = 'MW'

	esb = pd.read_excel(io.BytesIO(data), sheetname='Month_State', parse_cols='A:C,D:G')
	esb.columns = std_columns
	df_2011_2 = pd.melt(esb, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	df_2011_2.loc[:, 'sheet'] = 'Energy Sold Back'
	df_2011_2.loc[:, 'type'] = 'PV'
	df_2011_2.loc[:, 'units'] = 'MWh'

	count = pd.read_excel(io.BytesIO(data), sheetname='Month_State', parse_cols='A:C,N:Q')
	count.columns = std_columns
	df_2011_3 = pd.melt(count, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	df_2011_3.loc[:, 'sheet'] = 'Count'
	df_2011_3.loc[:, 'type'] = 'PV'
	df_2011_3.loc[:, 'units'] = '#'
	
	df = pd.concat([df_2011, df_2011_2, df_2011_3])	
	df.loc[:, 'nem'] = 'Yes'
	return df

if __name__ == '__main__':
	temp_df = get2011()
	print(temp_df.head())
