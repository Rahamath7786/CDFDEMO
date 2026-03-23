from django.contrib import admin
from django.urls import path

from cdfapp import views



urlpatterns = [
    path('assets/', views.getAssets, name='getAssets'),
    path('assetList/', views.assetsList, name='assetsList'),
    path('inverterTimeseries/', views.inverterTimeseries, name='inverter_timeseries'),

    path('dashboard/', views.dashboard, name='dashboard'),
]






