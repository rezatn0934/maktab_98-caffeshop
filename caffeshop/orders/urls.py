from django.contrib import admin
from django.urls import path
from . import views


app_name = "orders"
urlpatterns = [
    path('', views.cart1, name='cart'),
    path('update_or_remove', views.update_or_remove, name='update_or_remove'),
]