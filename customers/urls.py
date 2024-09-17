from django.urls import path
from . import views

app_name = 'customers'
urlpatterns = [
    path('get-cities', views.load_cities, name="get-cities"),
    path('get-districts', views.load_cities, name="get-districts"),
    path('get-villages', views.load_cities, name="get-villages")
]

