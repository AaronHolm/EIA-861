import requests
import pandas as pd
import io

def getCapacity(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheet_name='Monthly_Totals-States', skiprows=3, skip_footer=1, usecols="A:C,E:H")
	#sheet.rename(columns={'Year':'year', 'Month':'month', 'State':'state'}, inplace=True)
	sheet.columns=['year', 'month', 'state', 'Residential', 'Commercial', 'Industrial', 'Transportation']
	f2019cap = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	f2019cap['units'] = 'MW'
	f2019cap['nem'] = 'Yes'
	f2019cap['type'] = 'PV'
	f2019cap['sheet'] = 'Capacity'
	return f2019cap

def getStorageCapacity(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheet_name='Monthly_Totals-States', skiprows=3, skip_footer=1, usecols='A:C,O:R')
	#sheet.rename(columns={'Year':'year', 'Month':'month', 'State':'state'}, inplace=True)
	sheet.columns=['year', 'month', 'state', 'Residential', 'Commercial', 'Industrial', 'Transportation']
	f2019es = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	f2019es['units'] = 'MW'
	f2019es['nem'] = 'Yes'
	f2019es['type'] = 'PV'
	f2019es['sheet'] = 'Storage Capacity'
	return f2019es

def getEnergySoldBack(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheet_name='Monthly_Totals-States', skiprows=3, skip_footer=1, usecols="A:C,AI:AL")
	#sheet.rename(columns={'Year':'year','Month':'month','State':'state'}, inplace=True)
	sheet.columns = ['year', 'month', 'state', 'Residential', 'Commercial', 'Industrial', 'Transportation']
	f2019esb = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	f2019esb['units'] = 'MWh'
	f2019esb['nem'] = 'Yes'
	f2019esb['type'] = 'PV'
	f2019esb['sheet'] = 'Energy Sold Back'
	return f2019esb

def getCount(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheet_name='Monthly_Totals-States', skiprows=3, skip_footer=1, usecols="A:C,J:M")
	#sheet.rename(columns={'Year':'year','Month':'month','State':'state'}, inplace=True)
	sheet.columns = ['year', 'month', 'state', 'Residential', 'Commercial', 'Industrial', 'Transportation']
	f2019count = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	f2019count['units'] = "#"
	f2019count['nem'] = 'Yes'
	f2019count['type'] = 'PV'
	f2019count['sheet'] = 'Count'
	return f2019count

def getStorageCount(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheet_name="Monthly_Totals-States", skiprows=3, skip_footer=1, usecols="A:C,T:W")
	#sheet.rename(columns={'Year':'year', 'Month':'month', 'State':'state'}, inplace=True)
	sheet.columns=['year', 'month', 'state', 'Residential', 'Commercial', 'Industrial', 'Transportation']
	f20194 = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	f20194['units'] = '#'
	f20194['nem'] = 'Yes'
	f20194['type'] = 'PV'
	f20194['sheet'] = 'Storage Count'
	return f20194

def getVirtualCapacity(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheet_name="Monthly_Totals-States", skiprows=3, skip_footer=1, usecols="A:C,Y:AB")
	#sheet.rename(columns={'Year':'year', 'Month':'month', 'State':'state'}, inplace=True)
	sheet.columns=['year', 'month', 'state', 'Residential', 'Commercial', 'Industrial', 'Transportation']
	f20195 = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	f20195['units'] = 'MW'
	f20195['nem'] = 'Yes'
	f20195['type'] = 'PV'
	f20195['sheet'] = 'Virtual Capacity'
	return f20195

def getVirtualCount(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheet_name="Monthly_Totals-States", skiprows=3, skip_footer=1, usecols="A:C,AD:AG")
	#sheet.rename(columns={'Year':'year', 'Month':'month', 'State':'state'}, inplace=True)
	sheet.columns=['year', 'month', 'state', 'Residential', 'Commercial', 'Industrial', 'Transportation']
	f20196 = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	f20196['units'] = '#'
	f20196['nem'] = 'Yes'
	f20196['type'] = 'PV'
	f20196['sheet'] = 'Virtual Count'
	return f20196

def get2019():
	url = 'https://www.eia.gov/electricity/data/eia861m/xls/net_metering2019.xlsx'
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
	temp = get2019()
	temp.to_excel('/mnt/c/Users/AHolm/SEIA/OneDrive - SEIA/codebin/datasources/SEIA_DB/Outputs/eia861_2019Q1_1.xlsx')
	print(temp.head())
