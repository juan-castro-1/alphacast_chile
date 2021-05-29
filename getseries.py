#!/usr/bin/python
#author: jfernandezm

import zeep
import pandas as pd
from zeep.helpers import serialize_object
import datetime as dt
import numpy as np
from time import sleep
import sys

def consultaseries(user,pw,fInic,fFin,series):
    
    #Creación de inputs para conectar al webservice
    user=str(user)
    pw=str(pw)
    fInic=str(fInic)
    fFin=str(fFin)
    
    if type(series)==list:
        pass
    else:
        series=[str(series)]
        
    series=[x.upper() for x in series]
        
    #Se revisa si hay un código inválido. Todos debiesen terminar en d, m, t, o a (correspondiente a las frecuencias). En caso de ser inválido, se avisa al usuario y se retira de la lista a consultar
    for ser_cod in reversed(series):
        if ser_cod[-1].lower() in ["d","m","t","a"]:
            pass
        else:
            print("Serie " + ser_cod + " inexistente. Chequea el código")
            series.remove(ser_cod)
    
    #Se identifican las distintas frecuencias de series que pudieran existir y se clasifican por cada tipo.
    series_freq=[x[-1] for x in series]
    series_freq=list(np.unique(series_freq))
    
    #Ahora, se convierte la inicial de la frecuencia a su nombre, que es el que se necesita para hacer la consulta.
    
    for x in range(len(series_freq)):
        if series_freq[x]=="D":
            series_freq[x]=series_freq[x].replace("D","DAILY")
        elif series_freq[x]=="M":
            series_freq[x]=series_freq[x].replace("M","MONTHLY")
        elif series_freq[x]=="T":
            series_freq[x]=series_freq[x].replace("T","QUARTERLY")
        elif series_freq[x]=="A":
            series_freq[x]=series_freq[x].replace("A","ANNUAL")
        else:
            pass
    
    #Se identifica la dirección del WSDL (Web Service Definition Language) que permitirá a la librería zeep identificar qué consultas pueden hacerse al Webservice, además de generar el objeto client, que permitirá el intercambio de datos
    wsdl="https://si3.bcentral.cl/SieteWS/SieteWS.asmx?wsdl"
    client = zeep.Client(wsdl)
    
    #meta_series contendrá los datos recolectados y ordenados obtenidos desde "SearchSeries" para todas las frecuencias
    meta_series=pd.DataFrame()

    #Se itera dentro de la lista series_freq para consultar las distintas frecuencias de interés:
    for frequ in series_freq:#frequ=series_freq[0]
        for attempt in range(4):
            try:
                #Se consulta usando el usuario, password y frecuencia de interés
                res_search=client.service.SearchSeries(user,pw,frequ)
               #Se limpia la información obtenida
                res_search=res_search["SeriesInfos"]["internetSeriesInfo"]
                res_search = serialize_object(res_search)
                #Se crea un diccionario con las series obtenidas y los datos de interés (título, código y frencuencia)
                res_search = { serie_dict['seriesId']:[serie_dict['spanishTitle'],serie_dict['frequency']] for serie_dict in res_search }
                #A partir del diccionario creado, se arma un dataframe (meta_series_aux) que luego se agrega al dataframe
                #que contendrá todas las frecuencias (meta_series)
                meta_series_aux=pd.DataFrame.from_dict(res_search,orient='index')
                meta_series=meta_series.append(meta_series_aux)
                print("Frecuencia " + str(frequ) + " encontrada. Agregando")
                break
            except:
                print("Intento " + str(attempt) + ": La frecuencia " + str(frequ) + " no fue encontrada")
                #En caso de error, se esperan 20 segundos antes de volver a consultar la serie
                sleep(20)
        else:
            print("Frecuencia " + str(frequ) + " no fue encontrada. Deteniendo ejecución")
            sys.exit("Deteniendo ejecución")

    #Finalmente, se limpia el Dataframe obtenido para conservar sólo las series de interés:
    meta_series=meta_series.loc[series]
    meta_series.columns=["spanishTitle","frequency"]
    
    #Creación del DataFrame values_df, que incluirá todas las series que se consultarán.
    values_df=pd.DataFrame()
    #Iteración por cada una de las series consultando los datos. Los valores obtenidos se agregan a values_df
    for serieee in series:
        #Se genera un loop para hacer 10 intentos de consulta por serie. Si tiene éxito, continúa con la siguiente serie, si no tiene éxito, intenta nuevamente.
        for attempt in range(4):
            try:
                #Creación del objeto que contendrá el código de serie       
                ArrayOfString = client.get_type('ns0:ArrayOfString')
                value = ArrayOfString(serieee)
                
                #Se ejecuta la consulta utilizando los parámetros ingresados (usuario, password, fecha de inicio, fecha final y código de serie) y se asigna a la variable result
                result = client.service.GetSeries(user,pw,fInic,fFin, value)
                #Se omite la serie si no hay observaciones en el período solicitado
                if result["Series"]["fameSeries"][0]["obs"]==[]:
                    print("La serie "+ str(serieee) + " no tiene observaciones para el período seleccionado")
                    break
                #Se limpia la información obtenida, dejando como nombre de fila el código de serie y, como columnas, las fechas en formato dd-mm-aaaa
                result = serialize_object(result["Series"]["fameSeries"][0]["obs"])
                result=pd.DataFrame(result).T
                result.columns=result.iloc[0,:]
                result=result.drop(result.index[0:3],axis=0)
                result.index=[serieee]
                
                #Se agrega la serie ordenada al DataFrame values_df
                
                values_df=values_df.append(result,sort=True)
                print("Serie " + str(serieee) + " encontrada. Agregando")
                break
            except:
                print("Intento " + str(attempt) + ": La serie " + str(serieee) + " no fue encontrada")
                #En caso de error, se esperan 20 segundos antes de volver a consultar la serie
                sleep(20)
        else:
            print("La serie " + str(serieee) + " no fue encontrada. Omitiendo")
    
    #Se guarda en new_col los nombres de las columnas de values_df
    new_col=list(values_df.columns)
    #Se ordenan las fechas de new_col para asegurar su disposición desde la más antigua a la más nueva
    new_col.sort(key = lambda date: dt.datetime.strptime(date, '%d-%m-%Y'))
    #Se ordena el dataframe values_df con el orden descrito en la línea anterior
    values_df=values_df[new_col]
    #Se unen los resultados de meta_series con values_df en final_dic
    final_dic=pd.merge(meta_series,values_df,left_index=True,right_index=True)
    #Se separan las salidas para obtener un dataframe por frecuencia
    final_dic = dict(iter(final_dic.groupby('frequency')))
    final_dic.update((x, y.dropna(axis=1,how="all")) for x, y in final_dic.items())
    
    #Se devuelve el resultado de final_dic
    return final_dic