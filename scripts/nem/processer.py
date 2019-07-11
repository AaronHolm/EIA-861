import pandas as pd

#def processor(data, sheetname, skiprows, parsecols, units, nem, category):
#	sheet = pd.read_excel(data, sheetname=sheetname, skiprows=skiprows, parse_cols=parsecols)
#	df = process_cols(sheet)
#	out = pd.melt(df, id_vars['year', 'month', 'state'], value_vars=['Residential', 'Commercial', 'Industrial', 'Transportation'], var_name='sector', value_name='value')
#	out.loc[:, 'units'] = units
#	out.loc[:, 'nem'] = nem
#	out.loc[:, 'sheet'] = category
#	out.loc[:, 'type'] = 'PV'
#	out.loc[:, 'value'] = [float(x) if isinstance(x, (int, float)) else 0.0 for x in out['value']]
#	return out

def processer(df_in):
	df = pd.DataFrame()
	for state in df_in['state'].unique():
		t1 = df_in[df_in['state'] == state]
		sheets = pd.DataFrame()
		for sheet in t1['sheet'].unique():
			t2 = t1[t1['sheet'] == sheet]
			sectors = pd.DataFrame()
			for sector in t2['sector'].unique():
				t3 = t2[t2['sector'] == sector]
				temp = shifter(t3)
				sectors = pd.concat([sectors, temp])
				sectors.loc[:, 'incremental_positives'] = [x if x >=0 else 0 for x in sectors['incremental_value']]
				sectors.loc[:, 'incremental_negatives'] = [x if x < 0 else 0 for x in sectors['incremental_value']]
				years = pd.DataFrame()
				for year in sectors['year'].unique():
					y = sectors[sectors['year'] == year]
					y.loc[:, 'yearly_avg'] = y['incremental_negatives'].sum()/len(y[y['incremental_positives'] != 0]['incremental_positives'])
					years = pd.concat([years, y])
			sheets = pd.concat([sheets, years])
			#sheets = pd.concat([sheets, sectors])
		df = pd.concat([df, sheets])
	df.loc[:, 'result_value'] = [row['incremental_positives'] if row['incremental_positives'] == 0 else row['incremental_positives'] + row['yearly_avg'] for i, row in df.iterrows()]
	df = df[['state', 'sheet', 'nem', 'type', 'units', 'year', 'month', 'sector', 'cumulative_value', 'shifted_value', 'incremental_value', 'incremental_positives', 'incremental_negatives', 'yearly_avg', 'result_value']]
	return df

def shifter(df):
	df.sort_values(by=['state', 'sheet', 'sector', 'year', 'month', 'units'], inplace=True)
	df.loc[:, 'shifted'] = df['value'].shift(-1)
	
	#df.loc[:, 'shifted_value'] = df['shifted'] - df['value']
	df.loc[:, 'shifted_value'] = [row['shifted'] - row['value'] if (isinstance(row['shifted'], (int, float)) and isinstance(row['value'], (int, float))) else 0 for i, row in df.iterrows()]	

	df.loc[:, 'incremental_value'] = df['shifted_value'].shift(1)
	df.loc[:, 'incremental_value'] = [row['value'] if row['year'] == 2011 and row['month'] == 1 else row['incremental_value'] for i, row in df.iterrows()]
	df.rename(columns={'value':'cumulative_value'}, inplace=True)
	return df	
	

def process_cols(sheet):
	if('State' in sheet.columns):
		sheet.rename(columns={'State':'state'}, inplace=True)
	if('Year' in sheet.columns):
		sheet.rename(columns={'Year':'year'}, inplace=True)
	if('Month' in sheet.columns):
		sheet.renamce(columns={'Month':'month'}, inplace=True)
	return sheet
