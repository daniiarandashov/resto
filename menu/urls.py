from django.urls import path
from . import views


app_name = 'menu'

urlpatterns = [
    path('primary_meal/', views.PrimaryMealListView.as_view(), name='primary-meal'),
    path('wines/', views.WineListView.as_view(), name='wines'),
    
    
]