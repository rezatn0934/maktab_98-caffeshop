from django.contrib import admin
from django.urls import path
from . import views


app_name = "menu"
urlpatterns = [
    path('menu/', views.menu, name='menu'),
    path('show_product/<str:name>', views.product)
]