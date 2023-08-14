from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.StaffLogin.as_view(), name='login'),
    path('verify/', views.Verify.as_view(), name="verify"),
    path('logout/', views.logout_view, name="logout"),

    path('dashboard/', views.Dashboard.as_view(), name="dashboard"),

    path('result/', views.most_popular, name="result"),
    path('most_popular/', views.most_popular, name='most_popular'),
    path('peak_hour/', views.peak_business_hour, name='peak_business_hour'),


    path('orders/', views.Orders.as_view(), name='order_list'),
    path('orders/<int:pk>', views.OrderDetailView.as_view(), name='order_detail'),
    path('create_order_item/<int:pk>', views.CreateOrderItem.as_view(), name='create_order_detail'),
    path('delete_order_item/<int:pk>', views.delete_order_detail, name='delete_order_item'),
    path('confirm_order/<int:pk>', views.confirm_order, name='confirm_order'),
    path('cancel_order/<int:pk>', views.cancel_order, name='cancel_order'),
]
