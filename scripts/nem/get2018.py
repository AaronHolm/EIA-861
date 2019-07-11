import requests
import pandas as pd
import io

def getCapacity(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheetname='Monthly_Totals-States', skiprows=3, skip_footer=1, parse_cols="A:C,E:H")
	sheet.rename(columns={'Year':'year', 'Month':'month', 'State':'state'}, inplace=True)
	#sheet.columns=['year', 'month', 'state', 'Residential', 'Commercial', 'Industrial', 'Transportation']
	f2018cap = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	f2018cap['units'] = 'MW'
	f2018cap['nem'] = 'Yes'
	f2018cap['type'] = 'PV'
	f2018cap['sheet'] = 'Capacity'
	return f2018cap

def getStorageCapacity(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheetname='Monthly_Totals-States', skiprows=3, skip_footer=1, parse_cols='A:C,O:R')
	sheet.rename(columns={'Year':'year', 'Month':'month', 'State':'state'}, inplace=True)
	f2018es = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	f2018es['units'] = 'MW'
	f2018es['nem'] = 'Yes'
	f2018es['type'] = 'PV'
	f2018es['sheet'] = 'Storage Capacity'
	return f2018es

def getEnergySoldBack(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheetname='Monthly_Totals-States', skiprows=3, skip_footer=1, parse_cols="A:C,AI:AL")
	sheet.rename(columns={'Year':'year','Month':'month','State':'state'}, inplace=True)
	#sheet.columns = ['year', 'month', 'state', 'Residential', 'Commercial', 'Industrial', 'Transportation']
	f2018esb = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportationi'], var_name='sector', value_name='value')
	f2018esb['units'] = 'MWh'
	f2018esb['nem'] = 'Yes'
	f2018esb['type'] = 'PV'
	f2018esb['sheet'] = 'Energy Sold Back'
	return f2018esb

def getCount(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheetname='Monthly_Totals-States', skiprows=3, skip_footer=1, parse_cols="A:C,J:M")
	sheet.rename(columns={'Year':'year','Month':'month','State':'state'}, inplace=True)
	#sheet.columns = ['year', 'month', 'state', 'Residential', 'Commercial', 'Industrial', 'Transportation']
	f2018count = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	f2018count['units'] = "#"
	f2018count['nem'] = 'Yes'
	f2018count['type'] = 'PV'
	f2018count['sheet'] = 'Count'
	return f2018count

def getStorageCount(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheetname="Monthly_Totals-States", skiprows=3, skip_footer=1, parse_cols="A:C,T:W")
	sheet.rename(columns={'Year':'year', 'Month':'month', 'State':'state'}, inplace=True)
	f20184 = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	f20184['units'] = '#'
	f20184['nem'] = 'Yes'
	f20184['type'] = 'PV'
	f20184['sheet'] = 'Storage Count'
	return f20184

def getVirtualCapacity(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheetname="Monthly_Totals-States", skiprows=3, skip_footer=1, parse_cols="A:C,Y:AB")
	sheet.rename(columns={'Year':'year', 'Month':'month', 'State':'state'}, inplace=True)
	f20185 = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	f20185['units'] = 'MW'
	f20185['nem'] = 'Yes'
	f20185['type'] = 'PV'
	f20185['sheet'] = 'Virtual Capacity'
	return f20185

def getVirtualCount(url):
	data = requests.get(url).content
	sheet = pd.read_excel(io.BytesIO(data), sheetname="Monthly_Totals-States", skiprows=3, skip_footer=1, parse_cols="A:C,AD:AG")
	sheet.rename(columns={'Year':'year', 'Month':'month', 'State':'state'}, inplace=True)
	f20186 = pd.melt(sheet, id_vars=['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
	f20186['units'] = '#'
	f20186['nem'] = 'Yes'
	f20186['type'] = 'PV'
	f20186['sheet'] = 'Virtual Count'
	return f20186

def get2018():
	url = 'https://www.eia.gov/electricity/data/eia861m/archive/xls/net_metering2018.xlsx'
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
	temp = get2018()
	temp.to_excel('/mnt/c/Users/AHolm/SEIA/OneDrive - SEIA/codebin/datasources/SEIA_DB/Outputs/eia861_2018Q2_2.xlsx')
	print(temp.head())
