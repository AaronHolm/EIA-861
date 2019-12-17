import pandas as pd
import sqlalchemy as sa
from io import StringIO
from config import *

def to_sql(df):
  address = SQL_ADDRESS
  engine = sa.create_engine(address)
  con = engine.raw_connection()
  cursor = con.cursor()

  schema = 'markets'
  if_exists='replace'
  sep='\t'
  encoding='utf8'
  table='eia_826'
  df[:0].to_sql(table, engine, schema=schema, if_exists=if_exists, index=False)
  
  output = StringIO()
  df.to_csv(output, sep=sep, header=False, encoding=encoding, index=False)
  output.seek(0)

  cursor.copy_from(output, schema+'.'+table, sep=sep, null='')
  con.commit()
  con.close()
  return

def combine826():
  queryNEM = "SELECT state, year, month, sector, result_value as nem_value FROM markets.eia_826_nem where sheet = 'Capacity'"
  queryNonNEM = "SELECT state, year, month, sector, result_value as nonnem_value FROM markets.eia_826_nonnem where sheet = 'Photovoltaic'"

  engine = sa.create_engine(SQL_ADDRESS)
  nem = pd.read_sql(queryNEM, engine)
  nem['nem_value'] = nem['nem_value'].fillna(0)
  nonnem = pd.read_sql(queryNonNEM, engine)
  nonnem['nonnem_value'] = [pd.to_numeric(x) if isinstance(x, str) else x for x in nonnem['nonnem_value']]
  nonnem['nonnem_value'] = nonnem['nonnem_value'].fillna(0)
  writer = pd.ExcelWriter('/mnt/c/Users/AHolm/SEIA/OneDrive - SEIA/codebin/datasources/SEIA_DB/Outputs/tmp/eia826_debug.xlsx', engine='xlsxwriter')
  nem.to_excel(writer, sheet_name='nem')
  nonnem.to_excel(writer, sheet_name='nonnem')
  #eia826 = nem.merge(nonnem, how='outer', on=['state', 'year', 'month', 'sector'])
  eia826 = nem.merge(nonnem, how='left', on=['state', 'year', 'month', 'sector'])
  #eia826 = pd.concat([nem, nonnem])
  #eia826.to_excel(writer, sheet_name='eia826_premerge')
  eia826['nonnem_value'] = eia826['nonnem_value'].fillna(0)
  #print(nem.head(), '\n\n', nonnem.head())
  eia826['result_value'] = eia826['nem_value'] + eia826['nonnem_value']
  eia826.to_excel(writer, sheet_name='eia826_postmerge')
  writer.save()
  return eia826

if __name__ == '__main__':
  df = combine826()
  to_sql(df)
  df.to_excel('/mnt/c/Users/AHolm/SEIA/OneDrive - SEIA/codebin/datasources/SEIA_DB/Outputs/tmp/eia826_combined_2019Q1.xlsx')
