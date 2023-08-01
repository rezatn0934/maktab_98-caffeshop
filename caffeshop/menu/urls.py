from django.contrib import admin
from django.urls import path
from . import views


app_name = "menu"
urlpatterns = [
    path('menu/', views.menu, name='menu'),
    path('show_product/<str:name>', views.product, name='show_product'),
    path('search_product/', views.search_product, name='search_product'),
    path('search_result/', views.search_result, name='search_result')
]