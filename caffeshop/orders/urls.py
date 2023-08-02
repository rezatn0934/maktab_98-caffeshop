from django.contrib import admin
from django.urls import path
from . import views


app_name = "orders"
urlpatterns = [
    path('', views.cart, name='cart'),
    path('update_or_remove/', views.update_or_remove, name='update_or_remove'),
    path('create_order/', views.create_order, name='create_order'),
    path('history/', views.order_history, name="order_history")
]