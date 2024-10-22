import sqlite3
import pandas as pd

with sqlite3.connect('example.db') as conn:
    df = pd.read_sql(sql="SELECT * FROM Customers", con=conn)
    print(df)