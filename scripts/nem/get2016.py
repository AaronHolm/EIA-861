import requests
import pandas as pd
import io

def getCapacity(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheetname='Monthly_Totals-States', skiprows=3, skip_footer=1, parse_cols="A:H")
	sheet.rename(columns={'Year':'year', 'Month':'month', 'State':'state'}, inplace=True)
	#sheet.columns=['year', 'month', 'state', 'Residential', 'Commercial', 'Industrial', 'Transportation']
	f2016cap = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	f2016cap['units'] = 'MW'
	f2016cap['nem'] = 'Yes'
	f2016cap['type'] = 'PV'
	f2016cap['sheet'] = 'Capacity'
	return f2016cap

def getEnergySoldBack(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheetname='Monthly_Totals-States', skiprows=3, skip_footer=1, parse_cols="A:C,O:R")
	sheet.rename(columns={'Year':'year','Month':'month','State':'state'}, inplace=True)
	#sheet.columns = ['year', 'month', 'state', 'Residential', 'Commercial', 'Industrial', 'Transportation']
	f2016esb = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportationi'], var_name='sector', value_name='value')
	f2016esb['units'] = 'MWh'
	f2016esb['nem'] = 'Yes'
	f2016esb['type'] = 'PV'
	f2016esb['sheet'] = 'Energy Sold Back'
	return f2016esb

def getCount(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheetname='Monthly_Totals-States', skiprows=3, skip_footer=1, parse_cols="A:C,J:M")
	sheet.rename(columns={'Year':'year','Month':'month','State':'state'}, inplace=True)
	#sheet.columns = ['year', 'month', 'state', 'Residential', 'Commercial', 'Industrial', 'Transportation']
	f2016count = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	f2016count['units'] = "#"
	f2016count['nem'] = 'Yes'
	f2016count['type'] = 'PV'
	f2016count['sheet'] = 'Count'
	return f2016count

def get2016():
	url = 'https://www.eia.gov/electricity/data/eia861m/archive/xls/f826netmetering2016.xlsx'
	df_1 = getCapacity(url)
	df_2 = getEnergySoldBack(url)
	df_3 = getCount(url)
	
	df = pd.concat([df_1, df_2, df_3])
	#df.loc[:, 'value'] = [0 if isinstance(x, str) else x for x in df['value']]
	return df

if __name__ == '__main__':
	temp = get2016()
	print(temp.head())
