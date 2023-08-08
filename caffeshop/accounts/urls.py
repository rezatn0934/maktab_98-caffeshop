from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.StaffLogin.as_view(), name='login'),
    path('dashboard/', views.Dashboard.as_view(), name="dashboard"),
    path('verify/', views.Verify.as_view(), name="verify"),
    path('logout/', views.logout_view, name="logout"),
    path('orders/', views.Orders.as_view(), name='order_list'),
    path('confirm_order/<int:pk>', views.confirm_order, name='confirm_order'),
    path('cancel_order/<int:pk>', views.cancel_order, name='cancel_order'),
    path('delete_order_item/<int:pk>', views.delete_order_detail, name='delete_order_item'),
]
