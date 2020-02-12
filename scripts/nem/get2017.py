import requests
import pandas as pd
import io

def getCapacity(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheet_name='Monthly_Totals-States', skiprows=3, skip_footer=1, usecols="A:C,E:H")
	#sheet.rename(columns={'Year':'year', 'Month':'month', 'State':'state'}, inplace=True)
	sheet.columns=['year', 'month', 'state', 'Residential', 'Commercial', 'Industrial', 'Transportation']
	f2017cap = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	f2017cap['units'] = 'MW'
	f2017cap['nem'] = 'Yes'
	f2017cap['type'] = 'PV'
	f2017cap['sheet'] = 'Capacity'
	return f2017cap

def getStorageCapacity(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheet_name='Monthly_Totals-States', skiprows=3, skip_footer=1, usecols='A:C,O:R')
	#sheet.rename(columns={'Year':'year', 'Month':'month', 'State':'state'}, inplace=True)
	sheet.columns=['year', 'month', 'state', 'Residential', 'Commercial', 'Industrial', 'Transportation']
	f2017es = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	f2017es['units'] = 'MW'
	f2017es['nem'] = 'Yes'
	f2017es['type'] = 'PV'
	f2017es['sheet'] = 'Storage Capacity'
	return f2017es

def getEnergySoldBack(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheet_name='Monthly_Totals-States', skiprows=3, skip_footer=1, usecols="A:C,AI:AL")
	#sheet.rename(columns={'Year':'year','Month':'month','State':'state'}, inplace=True)
	sheet.columns = ['year', 'month', 'state', 'Residential', 'Commercial', 'Industrial', 'Transportation']
	f2017esb = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	f2017esb['units'] = 'MWh'
	f2017esb['nem'] = 'Yes'
	f2017esb['type'] = 'PV'
	f2017esb['sheet'] = 'Energy Sold Back'
	return f2017esb

def getCount(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheet_name='Monthly_Totals-States', skiprows=3, skip_footer=1, usecols="A:C,J:M")
	#sheet.rename(columns={'Year':'year','Month':'month','State':'state'}, inplace=True)
	sheet.columns = ['year', 'month', 'state', 'Residential', 'Commercial', 'Industrial', 'Transportation']
	f2017count = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	f2017count['units'] = "#"
	f2017count['nem'] = 'Yes'
	f2017count['type'] = 'PV'
	f2017count['sheet'] = 'Count'
	return f2017count

def getStorageCount(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheet_name="Monthly_Totals-States", skiprows=3, skip_footer=1, usecols="A:C,T:W")
	#sheet.rename(columns={'Year':'year', 'Month':'month', 'State':'state'}, inplace=True)
	sheet.columns=['year', 'month', 'state', 'Residential', 'Commercial', 'Industrial', 'Transportation']
	f20174 = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	f20174['units'] = '#'
	f20174['nem'] = 'Yes'
	f20174['type'] = 'PV'
	f20174['sheet'] = 'Storage Count'
	return f20174

def getVirtualCapacity(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheet_name="Monthly_Totals-States", skiprows=3, skip_footer=1, usecols="A:C,Y:AB")
	#sheet.rename(columns={'Year':'year', 'Month':'month', 'State':'state'}, inplace=True)
	sheet.columns=['year', 'month', 'state', 'Residential', 'Commercial', 'Industrial', 'Transportation']
	f20175 = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	f20175['units'] = 'MW'
	f20175['nem'] = 'Yes'
	f20175['type'] = 'PV'
	f20175['sheet'] = 'Virtual Capacity'
	return f20175

def getVirtualCount(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheet_name="Monthly_Totals-States", skiprows=3, skip_footer=1, usecols="A:C,AD:AG")
	#sheet.rename(columns={'Year':'year', 'Month':'month', 'State':'state'}, inplace=True)
	sheet.columns=['year', 'month', 'state', 'Residential', 'Commercial', 'Industrial', 'Transportation']
	f20176 = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	f20176['units'] = '#'
	f20176['nem'] = 'Yes'
	f20176['type'] = 'PV'
	f20176['sheet'] = 'Virtual Count'
	return f20176

def get2017():
	url = 'https://www.eia.gov/electricity/data/eia861m/archive/xls/net_metering2017.xlsx'
	df_1 = getCapacity(url)
	df_2 = getEnergySoldBack(url)
	df_3 = getCount(url)
	df_4 = getStorageCapacity(url)
	df_5 = getStorageCount(url)
	df_6 = getVirtualCapacity(url)
	df_7 = getVirtualCount(url)
	df = pd.concat([df_1, df_2, df_3, df_4, df_5, df_6, df_7])
	#df.loc[:, 'value'] = [0 if isinstance(x, str) else x for x in df['value']]
	return df

if __name__ == '__main__':
	temp = get2017()
	print(temp.head())
