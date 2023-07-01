
import requests
import pandas as pd
import numpy as np
from django.http import JsonResponse


columns = ['c_d_dep', 'departamento', 'c_d_mun', 'municipio', 'grupo_de_cultivo',
       'subgrupo_de_cultivo', 'cultivo', 'desagregaci_n_regional_y', 'a_o',
       'periodo', 'rea_sembrada_ha', 'rea_cosechada_ha', 'producci_n_t',
       'rendimiento_t_ha', 'estado_fisico_produccion', 'nombre_cientifico',
       'ciclo_de_cultivo']

df = pd.read_csv('static/cultivos_rendimiento.csv')
df.columns = columns
df = df[df['cultivo'] == 'CAFE']
df = df[['departamento', 'municipio', 'a_o', 'rea_sembrada_ha', 'rea_cosechada_ha', 'producci_n_t']]



def dataInZero():
    data_zero = df == 0
    return data_zero.sum().to_json()


def dataOutliders():
    area_s = total_outlider('rea_sembrada_ha', df)
    area_c = total_outlider('rea_cosechada_ha', df)
    prod = total_outlider('producci_n_t', df)
    outliders = {
        'rea_sembrada_ha': area_s,
        'rea_cosechada_ha': area_c,
        'producci_n_t': prod
    }
    return JsonResponse(outliders)


# DEFINICIÓN DE UNA FUNCIÓN PARA CALCULAR EL TOTAL DE DATOS ATÍPICOS DE UN ATRIBUTO
def total_outlider(atr, df):
    Q1 = np.percentile(df[atr], 25, method = 'midpoint')
    Q3 = np.percentile(df[atr], 75, method = 'midpoint')
    IQR = Q3 - Q1
    upper = df[atr] >= (Q3+1.5*IQR)
    lower = df[atr]<= (Q1-1.5*IQR)
    total_atipicos = sum(upper) + sum(lower)
    return total_atipicos
