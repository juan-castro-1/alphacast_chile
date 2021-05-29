import pandas as pd
from datetime import datetime

# armado de produccion
data = pd.read_excel('C:\\Users\\juan_\\Dropbox\\Mi PC (LAPTOP-H9MAOJRB)\\Desktop\\alphacast_chile\\produccion_new.xlsx')

cols = data.iloc[1]

df = data.iloc[2:]
df = df.rename(columns=cols)


df['Periodo'] = pd.to_datetime(df['Periodo'], errors='coerce').dt.strftime('%Y-%m-%d') 
df = df.set_index('Periodo')

# dos formas
prod_name = 'Índice de producción industrial '
df.columns = [prod_name + str(col)  for col in df.columns]
df = df.add_prefix(prod_name)

produccion = df


# armado de ventas
data = pd.read_excel('C:\\Users\\juan_\\Dropbox\\Mi PC (LAPTOP-H9MAOJRB)\\Desktop\\alphacast_chile\\ventas_new.xlsx')

cols = data.iloc[1]

df = data.iloc[2:]
df = df.rename(columns=cols)

df['Periodo'] = pd.to_datetime(df['Periodo'], errors='coerce').dt.strftime('%Y-%m-%d') 
df = df.set_index('Periodo')

# dos formas
ventas_name = 'Índice de ventas industrial '
df.columns = [ventas_name + str(col)  for col in df.columns]
df = df.add_prefix(ventas_name)

ventas = df

