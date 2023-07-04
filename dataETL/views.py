
from django.shortcuts import render
from django.http import HttpResponse
from .analysis.statistic import resumeStatistic, misingData, allDataInZero, getDept, getMun, getCodDept, getCodMun, headData
from .analysis.cleaning import dataInZero, dataOutliders
from .analysis.model_logistic import clean_data, make_prediction
from .analysis.model_lineal import make_prediction_lineal

# Create your views here.

def getListDept(request):
    return HttpResponse(getDept())

def getListMun(request, departamento):
    return HttpResponse(getMun(departamento))

def getCodigoDept(request, departamento):
    return HttpResponse(getCodDept(departamento))

def getCodigoMun(request, municipio):
    return HttpResponse(getCodMun(municipio))

def resumeState(request):
    return HttpResponse(resumeStatistic())

def allDataZero(request):
    return HttpResponse(allDataInZero())

def dataZero(request):
    return HttpResponse(dataInZero())

def misingDt(request):
    return HttpResponse(misingData())

def dataOut(request):
    return HttpResponse(dataOutliders())

def dataClean(request):
    return HttpResponse(clean_data())

def headerData(request):
    return HttpResponse(headData())

def prediction(request, departamento, municipio, periodo, siembra):
    return HttpResponse(make_prediction(departamento, municipio, periodo, siembra))

def prediction_lineal(request, departamento, municipio, periodo, siembra):
    return HttpResponse(make_prediction_lineal(departamento, municipio, periodo, siembra))
