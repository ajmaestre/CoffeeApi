
import requests
import pandas as pd
import numpy as np
from django.http import JsonResponse

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, precision_recall_fscore_support, confusion_matrix
from sklearn.model_selection import train_test_split


# RENOMBRAMOS LAS COLUMNAS DEL DATA SET
columns = ['c_d_dep', 'departamento', 'c_d_mun', 'municipio', 'grupo_de_cultivo',
       'subgrupo_de_cultivo', 'cultivo', 'desagregaci_n_regional_y', 'a_o',
       'periodo', 'rea_sembrada_ha', 'rea_cosechada_ha', 'producci_n_t',
       'rendimiento_t_ha', 'estado_fisico_produccion', 'nombre_cientifico',
       'ciclo_de_cultivo']

# EXTRAEMOS EL DATASET
df = pd.read_csv('static/cultivos_rendimiento.csv')
df.columns = columns

# SELECCIONAMOS EL CONJUNTO DE DATOS QUE SOLO CORRESPONDE AL CULTIVO DE CAFÉ
df = df[df['cultivo'] == 'CAFE']


# SELECCIÓN DE LOS DATOS
# CONVERTIMOS LOS ATRIBUTOS DEPARTAMENTO Y MUNICIPIO A NUMÉRICOS 
# (PARA ELLO ESCOGEMOS LOS CÓDIGOS DE LOS DEPARTAMENTOS Y LOS MUNICIPIOS, YA QUE SON ÚNICOS Y NUMÉRICOS)
df = df[['c_d_dep', 'c_d_mun', 'a_o', 'rea_sembrada_ha', 'rea_cosechada_ha', 'producci_n_t']]


# RENOMBRAMOS LAS COLUMNAS DEL DATA SET
columns = ['departamento', 'municipio', 'periodo', 'siembra', 'cosecha', 'produccion']
df.columns = columns


# ELIMINACIÓN DE DATOS IGUALES A CERO
df = df[~(df == 0).any(axis=1)]


# DEFINICIÓN DE UNA FUNCIÓN PARA CALCULAR EL TOTAL DE DATOS ATÍPICOS DE UN ATRIBUTO
def total_outlider(atr, df):
    Q1 = np.percentile(df[atr], 25, method = 'midpoint')
    Q3 = np.percentile(df[atr], 75, method = 'midpoint')
    IQR = Q3 - Q1
    upper = df[atr] >= (Q3+1.5*IQR)
    lower = df[atr]<= (Q1-1.5*IQR)
    total_atipicos = sum(upper) + sum(lower)
    return total_atipicos


# DEFINICIÓN DE UNA FUNCIÓN PARA ELIMINAR LOS DATOS ATÍPICOS DE UN ATRIBUTO
def delete_outlider(atr, df):
    data = df
    mean = data[atr].mean()
    while True:
        Q1 = np.percentile(data[atr], 25, method = 'midpoint')
        Q3 = np.percentile(data[atr], 75, method = 'midpoint')
        IQR = Q3 - Q1
        # data[~((data[atr] <= (Q3+0.3*IQR)) & (data[atr] >= (Q1-0.3*IQR)))] = mean
        data.loc[~((data[atr] <= (Q3+1.5*IQR)) & (data[atr] >= (Q1-1.5*IQR))), atr] = mean
        total_atip = total_outlider(atr, data)
        if total_atip == 0:
            return data


# DEFINICIÓN DE UNA FUNCIÓN PARA REEMPLAZAR LOS DATOS ATÍPICOS DE UN ATRIBUTO USANDO UNA RECTA DE REGRESIÓN
def replace_outlider(atry, atrx, df):
    data = df
    while True:
        Q1 = np.percentile(data[atry], 25, method = 'midpoint')
        Q3 = np.percentile(data[atry], 75, method = 'midpoint')
        IQR = Q3 - Q1
        xy = data[atrx]*data[atry]
        xx = data[atrx]*data[atrx]
        x_total = data[atrx].sum()
        y_total = data[atry].sum()
        xy_total = np.sum(xy)
        xx_total = np.sum(xx)
        n = data[atrx].shape[0]
        m = ((n*xy_total) - (x_total*y_total)) / ((n*xx_total) - (np.power(x_total, 2)))
        b = ((y_total*xx_total) - (x_total*xy_total)) / ((n*xx_total) - (np.power(x_total, 2)))
        data.loc[~((data[atry] <= (Q3+1.5*IQR)) & (data[atry] >= (Q1-1.5*IQR))), atry] = (data[atrx]*m) + b
        total_atip = total_outlider(atry, data)
        if total_atip == 0:
            return data

# ELIMINACIÓN DE DATOS ATÍPICOS EN EL ATRIBUTO ÁREA COSECHADA
df = delete_outlider('cosecha', df)
# ELIMINACIÓN DE DATOS ATÍPICOS EN EL ATRIBUTO ÁREA SEMBRADA
df = replace_outlider('siembra', 'cosecha', df)
# ELIMINACIÓN DE DATOS ATÍPICOS EN EL ATRIBUTO PRODUCCIÓN
df = replace_outlider('produccion', 'cosecha', df)
# CATEGORIZACIÓN DEL ATRIBUTO PRODUCCIÓN
mean_prod = df['produccion'].mean()
df['produccion'] = df['produccion'] >= mean_prod


# CREAMOS UNA FUNCIÓN PARA RETORNAR EL DATASET YA LIMPIO
def clean_data():
    return df


# --------------------------------------------- CONSTRUCCIÓN DEL MODELO -----------------------------------------

# CREAMOS UNA REFERENCIA AL ALGORITMO DE REGRESIÓN LOGISTICA
model = LogisticRegression()
# DIVIDIMOS LOS ATRIBUTOS EN DESCRIPTIVOS Y OBJETIVO
X = df[['departamento', 'municipio', 'periodo', 'siembra']].values
y = df['produccion'].values
# DIVIDIMOS LOS DATOS EN DATOS DE PRUEBA Y DATOS DE ENTRENAMIENTO AL 75%
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.75, random_state=27) 
# CONSTRUIMOS EL MODELO DE PREDICCIÓN
model.fit(X_train, y_train)


# CREAMOS UNA FUNCIÓN PARA REALIZAR PREDICCIONES
def make_prediction(departamento, municipio, periodo, siembra): 
    prediction = model.predict([[departamento, municipio, periodo, siembra]])
    if prediction:
        return JsonResponse({ 'response': 'Alta'})
    return JsonResponse({ 'response': 'Baja' })






