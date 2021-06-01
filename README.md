# Alphacast Chile

En este README se detallan lo pasos realizados en el script de get_data.py para la carga, transformación y exportación de los indicadores industriales de Chile a un .csv

### Importación de paquete

Se importan todos los paquetes necesarios para el código, detallados en requirements.txt

### Sincronización con API del Banco Central de Chile

Se corré el código del BCCh getseries.py donde se crea la función `consultaseries(user,pw,fInic,fFin,series)` para consultar los datos del organizmo. Luego se corre el credentials.py donde estan mis credenciales, user y password, ignorado en GitHub con el .gitignore aproposito para que no sean públicas. Se determinan las fechas y códigos de las variables a utilizar.


### Fecha e Index

Para ambos DataFrames, usando `datetime` cambiamos el formato de la fecha a `strftime('%Y-%m-%d')` para luego usarlo como `index` del DataFrame.

Adicionalmente agregamos un prefijo con el nombre del Índice utilizado a todas las variables según corresponda:

- Índice de producción industrial
- Índice de ventas industrial

*Note: esta parte ya estaba hecha, ya que al bajar los datos de la API las variables se llaman como la base de datos. Igual deje en el código muteado como sería agregarle un prefix.

### Join

Luego realizamos un `join` de ambos DataFrames con el index.

### Moving Average

Se estima la rolling Moving Average de 12 periodos de la variable:

- Índice de Producción industrial, INE (base 2014=100)

Se presenta un pequeño plot usando `matplotlib.pyplot` para ver a ojo el fit de la misma.

### De DataFrame a .csv

Finalmente se exporta el DataFrame con todas las variables y la MA a un .csv






