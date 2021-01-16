from django.urls import path
from . import views


app_name = 'reservation'


urlpatterns = [
    path('', views.reservation, name='reservation'),
    path('my_reservations/', views.user_orders, name='my_reservations'),
]
