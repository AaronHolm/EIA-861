import requests
import pandas as pd
import io

def getCapacity(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheet_name='Monthly Totals-States', skiprows=3, skip_footer=1, usecols="A:C,E:H")
	#sheet.rename(columns={'Year':'year', 'Month':'month', 'State':'state'}, inplace=True)
	sheet.columns=['year', 'month', 'state', 'Residential', 'Commercial', 'Industrial', 'Transportation']
	f2014cap = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	f2014cap['units'] = 'MW'
	f2014cap['nem'] = 'Yes'
	f2014cap['type'] = 'PV'
	f2014cap['sheet'] = 'Capacity'
	return f2014cap

def getEnergySoldBack(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheet_name='Monthly Totals-States', skiprows=3, skip_footer=1, usecols="A:C,O:R")
	#sheet.rename(columns={'Year':'year','Month':'month','State':'state'}, inplace=True)
	sheet.columns = ['year', 'month', 'state', 'Residential', 'Commercial', 'Industrial', 'Transportation']
	f2014esb = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	f2014esb['units'] = 'MWh'
	f2014esb['nem'] = 'Yes'
	f2014esb['type'] = 'PV'
	f2014esb['sheet'] = 'Energy Sold Back'
	return f2014esb

def getCount(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheet_name='Monthly Totals-States', skiprows=3, skip_footer=1, usecols="A:C,J:M")
	#sheet.rename(columns={'Year':'year','Month':'month','State':'state'}, inplace=True)
	sheet.columns = ['year', 'month', 'state', 'Residential', 'Commercial', 'Industrial', 'Transportation']
	f2014count = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	f2014count['units'] = "#"
	f2014count['nem'] = 'Yes'
	f2014count['type'] = 'PV'
	f2014count['sheet'] = 'Count'
	return f2014count

def get2014():
	url = 'https://www.eia.gov/electricity/data/eia861m/archive/xls/f826netmetering2014.xls'
	df_1 = getCapacity(url)
	df_2 = getEnergySoldBack(url)
	df_3 = getCount(url)
	
	df = pd.concat([df_1, df_2, df_3])
	#df.loc[:, 'value'] = [0 if isinstance(x, str) else x for x in df['value']]
	return df

if __name__ == '__main__':
	temp = get2014()
	print(temp.head())
