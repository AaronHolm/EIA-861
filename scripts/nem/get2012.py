import requests
import pandas as pd
import io

def getCapacity(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheetname='Month_State', parse_cols="A:C,I:L")
	sheet.columns=['year', 'month', 'state', 'Residential', 'Commercial', 'Industrial', 'Transportation']
	f2012cap = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	f2012cap['units'] = 'MW'
	f2012cap['nem'] = 'Yes'
	f2012cap['type'] = 'PV'
	f2012cap['sheet'] = 'Capacity'
	return f2012cap

def getEnergySoldBack(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheetname='Month_State', parse_cols="A:G")
	sheet.columns = ['year', 'month', 'state', 'Residential', 'Commercial', 'Industrial', 'Transportation']
	f2012esb = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportationi'], var_name='sector', value_name='value')
	f2012esb['units'] = 'MWh'
	f2012esb['nem'] = 'Yes'
	f2012esb['type'] = 'PV'
	f2012esb['sheet'] = 'Energy Sold Back'
	return f2012esb

def getCount(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheetname='Month_State', parse_cols="A:C,N:Q")
	sheet.columns = ['year', 'month', 'state', 'Residential', 'Commercial', 'Industrial', 'Transportation']
	f2012count = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	f2012count['units'] = "#"
	f2012count['nem'] = 'Yes'
	f2012count['type'] = 'PV'
	f2012count['sheet'] = 'Count'
	return f2012count

def get2012():
	url = 'https://www.eia.gov/electricity/data/eia861m/archive/xls/f826netmetering2012.xls'
	df_1 = getCapacity(url)
	df_2 = getEnergySoldBack(url)
	df_3 = getCount(url)
	
	df = pd.concat([df_1, df_2, df_3])
	return df

if __name__ == '__main__':
	temp = get2012()
	print(temp.head())
