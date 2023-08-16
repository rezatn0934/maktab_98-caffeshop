from django.contrib import admin
from django.urls import path
from . import views


app_name = "menu"
urlpatterns = [
    path('menu/', views.Menu.as_view(), name='menu'),
    path('show_product/<int:pk>', views.ProductView.as_view(), name='show_product'),
    path('search/', views.search_product_view, name='search'),
]