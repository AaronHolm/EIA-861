import pandas as pd
import requests
import sqlalchemy as sa
from io import StringIO

from scripts.sales_revenue import sales_revenue
from scripts.to_sql import to_sql

from config import SQL_ADDRESS

def Sales_and_Revenue():
  engine = sa.create_engine(SQL_ADDRESS)

  df = sales_revenue()
  to_sql(df, engine, 'markets', 'eia_861_sales_revenue', '\t', 'replace')
  return

if __name__ == '__main__':
  Sales_and_Revenue()
