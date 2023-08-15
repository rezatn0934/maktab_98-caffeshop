from django.contrib import admin
from django.urls import path
from . import views


app_name = "orders"
urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),
    path('create_order/', views.create_order, name='create_order'),
    path('history/', views.order_history, name="order_history"),
    path('cancel_order_by_customer/<int:pk>', views.cancel_order_by_customer, name='cancel_order_by_customer'),
]