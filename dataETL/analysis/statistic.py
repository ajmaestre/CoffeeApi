
import pandas as pd
import numpy as np


columns = ['c_d_dep', 'departamento', 'c_d_mun', 'municipio', 'grupo_de_cultivo',
       'subgrupo_de_cultivo', 'cultivo', 'desagregaci_n_regional_y', 'a_o',
       'periodo', 'rea_sembrada_ha', 'rea_cosechada_ha', 'producci_n_t',
       'rendimiento_t_ha', 'estado_fisico_produccion', 'nombre_cientifico',
       'ciclo_de_cultivo']

df = pd.read_csv('static/cultivos_rendimiento.csv')
df.columns = columns
df = df[df['cultivo'] == 'CAFE']


# CREAMOS UNA FUNCIÓN PARA RETORNAR LA LISTA DE DEPARTAMENTOS
def getDept():
    data = df[['departamento', 'municipio']]
    dept = data.groupby('departamento').count()
    return dept.to_json()


# CREAMOS UNA FUNCIÓN PARA RETORNAR EL CÓDIGO DE UN DEPARTAMENTO
def getCodDept(departamento):
    data = df[['departamento', 'c_d_dep']]
    data = data[data['departamento'] == departamento]
    cod_dept = data.groupby('c_d_dep').count()
    return cod_dept.to_json()


# CREAMOS UNA FUNCIÓN PARA RETORNAR EL CÓDIGO DE UN MUNICIPIO
def getCodMun(municipio):
    data = df[['municipio', 'c_d_mun']]
    data = data[data['municipio'] == municipio]
    cod_mun = data.groupby('c_d_mun').count()
    return cod_mun.to_json()


# CREAMOS UNA FUNCIÓN PARA RETORNAR LA LISTA DE MUNICIPIOS DE UN DEPARTAMENTO
def getMun(departamento):
    data = df[['departamento', 'municipio']]
    data = data[data['departamento'] == departamento]
    mun = data.groupby('municipio').count()
    return mun.to_json()
    

# CREAMOS UNA FUNCIÓN PARA RETORNAR EL RESUMEN ESTADISTICO DEL DATASET
def resumeStatistic():
    return df.describe().round(2).to_json()


# CREAMOS UNA FUNCIÓN PARA RETORNAR LOS DATOS CON VALORES EN CERO DEL DATASET
def allDataInZero():
    df_zero = df[['c_d_dep', 'c_d_mun', 'a_o', 'rea_sembrada_ha', 'rea_cosechada_ha', 'producci_n_t', 'rendimiento_t_ha']]
    data_zero = df_zero == 0
    return data_zero.sum().to_json()


# CREAMOS UNA FUNCIÓN PARA RETORNAR LOS DATOS FALTANTES DEL DATASET
def misingData():
    return df.isna().sum().to_json()

# CREAMOS UNA FUNCIÓN PARA RETORNAR LAS 10 PRIMERAS INSTANCIAS DEL DATASET
def headData():
    return df.head().to_json()