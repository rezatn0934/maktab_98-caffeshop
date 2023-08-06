from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.StaffLogin.as_view(), name='login'),
    path('dashboard/', views.Dashboard.as_view(), name="dashboard"),
    path('verify/', views.Verify.as_view(), name="verify"),
    path('logout/', views.logout, name="logout"),
    path('orders', views.Orders.as_view(), name='order_list')
]