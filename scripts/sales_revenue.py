import requests
import pandas as pd

def sales_revenue():
  url = 'https://www.eia.gov/electricity/data/eia861m/xls/sales_revenue.xlsx'
  r = requests.get(url)
  file = r.content
  settings = {0: {'sector': 'Residential', 'cols': 'A:H'},
              1: {'sector': 'Commercial', 'cols': 'A:D,I:L'},
              2: {'sector': 'Industrial', 'cols': 'A:D,M:P'},
              3: {'sector': 'Transportation', 'cols': 'A:D,Q:T'},
              4: {'sector': 'Other', 'cols': 'A:D,U:X'},
              5: {'sector': 'Total', 'cols': 'A:D,Y:AB'}}
  dfs = []
  for k,v in settings.items():
    df = file_parser(file, settings[k]['cols'], settings[k]['sector'])
    dfs.append(df)
  df = pd.concat(dfs)
  return df

def file_parser(file, cols, sector):
  tmp_df = pd.read_excel(file, skipfooter=1, skiprows=2, usecols=cols)
  tmp_df.columns = ['year', 'month', 'state_abbr', 'data_status', 'revenue', 'sales', 'customers', 'price']
  units_dict = {'revenue':'thousand dollars', 'sales':'megawatt hours', 'customers':'count', 'price':'cents/kWh'}
  dfs = []
  for k,v in units_dict.items():
    abbr_columns = ['year', 'month', 'state_abbr', 'data_status', k]
    df = tmp_df[abbr_columns]
    df.rename(columns={k:'value'}, inplace=True)
    df.loc[:, 'type'] = k
    df.loc[:, 'units'] = v
    dfs.append(df)
  df = pd.concat(dfs)
  df.loc[:, 'sector'] = sector
  return df

if __name__ == '__main__':
  sales_revenue()
