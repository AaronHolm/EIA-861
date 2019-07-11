import requests
import pandas as pd
import io

def getCapacity(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheetname='Monthly Totals-States', skiprows=3, skip_footer=1, parse_cols="A:H")
	sheet.rename(columns={'Year':'year', 'Month':'month', 'State':'state'}, inplace=True)
	#sheet.columns=['year', 'month', 'state', 'Residential', 'Commercial', 'Industrial', 'Transportation']
	f2015cap = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	f2015cap['units'] = 'MW'
	f2015cap['nem'] = 'Yes'
	f2015cap['type'] = 'PV'
	f2015cap['sheet'] = 'Capacity'
	return f2015cap

def getEnergySoldBack(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheetname='Monthly Totals-States', skiprows=3, skip_footer=1, parse_cols="A:C,O:R")
	sheet.rename(columns={'Year':'year','Month':'month','State':'state'}, inplace=True)
	#sheet.columns = ['year', 'month', 'state', 'Residential', 'Commercial', 'Industrial', 'Transportation']
	f2015esb = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportationi'], var_name='sector', value_name='value')
	f2015esb['units'] = 'MWh'
	f2015esb['nem'] = 'Yes'
	f2015esb['type'] = 'PV'
	f2015esb['sheet'] = 'Energy Sold Back'
	return f2015esb

def getCount(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheetname='Monthly Totals-States', skiprows=3, skip_footer=1, parse_cols="A:C,J:M")
	sheet.rename(columns={'Year':'year','Month':'month','State':'state'}, inplace=True)
	#sheet.columns = ['year', 'month', 'state', 'Residential', 'Commercial', 'Industrial', 'Transportation']
	f2015count = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	f2015count['units'] = "#"
	f2015count['nem'] = 'Yes'
	f2015count['type'] = 'PV'
	f2015count['sheet'] = 'Count'
	return f2015count

def get2015():
	url = 'https://www.eia.gov/electricity/data/eia861m/archive/xls/f826netmetering2015.xls'
	df_1 = getCapacity(url)
	df_2 = getEnergySoldBack(url)
	df_3 = getCount(url)
	
	df = pd.concat([df_1, df_2, df_3])
	#df.loc[:, 'value'] = [0 if isinstance(x, str) else x for x in df['value']]
	return df

if __name__ == '__main__':
	temp = get2015()
	print(temp.head())
