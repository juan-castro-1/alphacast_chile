import pandas as pd
from datetime import datetime
import os, sys

os.chdir('C:\\Users\\juan_\\Dropbox\\Mi PC (LAPTOP-H9MAOJRB)\\Desktop\\alphacast_chile')
exec(open('getseries.py').read())
exec(open('credentials.py').read())
f_init = '2003-01-01'
f_fin = '2021-04-01'


# PRODUCCION

S = ['F034.PRN.IND.INE.2014.0.M',
     'F034.PRN.IND.INE.2009.0.M',
     'F034.PRN.IND.SOF.2014.0.M',
     'F034.PRN.IND.SOF.2003.0.M',
     'F034.PRN.IND.SOF.2000.0.M',
     'F034.PRN.IND.SOF.2000.0.M']


a = consultaseries(user,
               password,
               f_init,
               f_fin,
               S)

df = a.get('MONTHLY')
df = df.T
cols = df.loc['spanishTitle']
df = df.loc['01-12-2003':]
df.columns = cols

df.index = pd.to_datetime(df.index, errors='coerce').strftime('%Y-%m-%d')

# agregar prefix
#prod_name = 'Índice de producción industrial '
#df.columns = [prod_name + str(col)  for col in df.columns]
#df = df.add_prefix(prod_name)

produccion = df

# VENTAS

S = ['F034.VTI.IND.SOF.2014.0.M',
     'F034.VTI.IND.SOF.2003.0.M',
     'F034.VTI.IND.SOF.2000.0.M' ]

a = consultaseries(user,
               password,
               f_init,
               f_fin,
               S)

df = a.get('MONTHLY')
df = df.T
cols = df.loc['spanishTitle']
df = df.loc['01-12-2003':]
df.columns = cols

df.index = pd.to_datetime(df.index, errors='coerce').strftime('%Y-%m-%d')

# agregar prefix
#ventas_name = 'Índice de ventas industrial '
#df.columns = [ventas_name + str(col)  for col in df.columns]
#df = df.add_prefix(ventas_name)

ventas = df

# join
df = produccion.join(ventas, on=ventas.index).astype(float)

# MA 
windw = 12
df['MA'] = df['Índice de producción industrial, INE (base 2014=100)'].rolling(window=windw).mean()

# plot
from matplotlib import pyplot as plt
ma = pd.DataFrame(df['MA'])
ma['real'] = df['Índice de producción industrial, INE (base 2014=100)']
ma.plot()
plt.show()

# exportar dataframe final a csv
df.to_csv(r'C:\\Users\\juan_\\Dropbox\\Mi PC (LAPTOP-H9MAOJRB)\\Desktop\\alphacast_chile\\data.csv')



