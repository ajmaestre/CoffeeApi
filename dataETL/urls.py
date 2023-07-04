
from django.urls import path, register_converter
from . import views
from .analysis.convert import FloatUrlParameterConverter

register_converter(FloatUrlParameterConverter, 'float')

urlpatterns = [
    path('list-department', views.getListDept, name='index'),
    path('list-municipio/<departamento>', views.getListMun, name='index'),
    path('code-department/<departamento>', views.getCodigoDept, name='index'),
    path('code-municipio/<municipio>', views.getCodigoMun, name='index'),
    path('resume-statistic', views.resumeState, name='index'),
    path('mising-data', views.misingDt, name='index'),
    path('data-zeros', views.dataZero, name='index'),
    path('data-outliders', views.dataOut, name='index'),
    path('all-data-zeros', views.allDataZero, name='index'),
    path('all-data-clean', views.dataClean, name='index'),
    path('head-data', views.headerData, name='index'),
    path('prediction/<int:departamento>/<int:municipio>/<int:periodo>/<float:siembra>', views.prediction, name='index'),
    path('prediction-lineal/<int:departamento>/<int:municipio>/<int:periodo>/<float:siembra>', views.prediction_lineal, name='index'),
]