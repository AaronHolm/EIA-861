import requests
import pandas as pd
import io

def getCapacity(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheet_name='State Totals-All Months', skiprows=3, usecols="A:C,E:H")
	#sheet.rename(columns={'Year':'year', 'Month':'month', 'State':'state'}, inplace=True)
	sheet.columns=['year', 'month', 'state', 'Residential', 'Commercial', 'Industrial', 'Transportation']
	f2013cap = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	f2013cap['units'] = 'MW'
	f2013cap['nem'] = 'Yes'
	f2013cap['type'] = 'PV'
	f2013cap['sheet'] = 'Capacity'
	return f2013cap

def getEnergySoldBack(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheet_name='State Totals-All Months', skiprows=3, usecols="A:C,O:R")
	#sheet.rename(columns={'Year':'year','Month':'month','State':'state'}, inplace=True)
	sheet.columns = ['year', 'month', 'state', 'Residential', 'Commercial', 'Industrial', 'Transportation']
	f2013esb = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	f2013esb['units'] = 'MWh'
	f2013esb['nem'] = 'Yes'
	f2013esb['type'] = 'PV'
	f2013esb['sheet'] = 'Energy Sold Back'
	return f2013esb

def getCount(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheet_name='State Totals-All Months', skiprows=3, usecols="A:C,J:M")
	#sheet.rename(columns={'Year':'year','Month':'month','State':'state'}, inplace=True)
	sheet.columns = ['year', 'month', 'state', 'Residential', 'Commercial', 'Industrial', 'Transportation']
	f2013count = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	f2013count['units'] = "#"
	f2013count['nem'] = 'Yes'
	f2013count['type'] = 'PV'
	f2013count['sheet'] = 'Count'
	return f2013count

def get2013():
	url = 'https://www.eia.gov/electricity/data/eia861m/archive/xls/f826netmetering2013.xls'
	df_1 = getCapacity(url)
	df_2 = getEnergySoldBack(url)
	df_3 = getCount(url)
	
	df = pd.concat([df_1, df_2, df_3])
	#df.loc[:, 'value'] = [0 if isinstance(x, str) else x for x in df['value']]
	return df

if __name__ == '__main__':
	temp = get2013()
	print(temp.head())
