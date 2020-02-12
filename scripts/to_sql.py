from io import StringIO

def to_sql(df, engine, schema, table, sep, if_exists):
  df[:0].to_sql(table, engine, schema=schema, if_exists=if_exists, index=False)

  output = StringIO()
  df.to_csv(output, sep=sep, header=False, encoding='utf8', index=False)
  output.seek(0)

  connection = engine.raw_connection()
  cursor = connection.cursor()
  cursor.copy_from(output, schema+'.'+table, sep=sep, null='')

  connection.commit()
  cursor.close()
  return
