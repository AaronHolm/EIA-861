import sqlalchemy as sa
import pandas as pd
from io import StringIO

def to_sql(gen):
	address = 'postgresql://PG:PGAH17@data.seia.org:5432/seia'
	engine = sa.create_engine(address)
	con = engine.raw_connection()
	cursor = con.cursor()

	schema = 'markets'
	if_exists = 'replace'
	sep='\t'
	encoding='utf8'
	table='eia_826_nem'
	gen[:0].to_sql(table, engine, schema=schema, if_exists=if_exists, index=False)
	
	output = StringIO()
	gen.to_csv(output, sep=sep, header=False, encoding=encoding, index=False)
	output.seek(0)

	cursor.copy_from(output, schema+'.'+table, sep=sep, null='')
	con.commit()
	con.close()
	print('Sent.')
	return
