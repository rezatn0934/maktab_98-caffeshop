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
    path('top_selling/', views.top_selling, name='top_selling'),
    path('hourly_sales/', views.hourly_sales, name='hourly_sales'),
    path('daily_sales/', views.daily_sales, name='daily_sales'),
    path('monthly_sales/', views.monthly_sales, name='monthly_sales'),
    path('yearly_sales/', views.yearly_sales, name='yearly_sales'),
    path('customer_sales/', views.customer_sales, name='customer_sales'),
    path('sales_by_category/', views.sales_by_category, name='sales_by_category'),
    path('order_status_report/', views.order_status_report, name='order_status_report'),
    path('customer_order_history/', views.customer_order_history, name='customer_order_history'),
    path('sales_by_employee_report/', views.sales_by_employee_report, name='sales_by_employee_report'),


    path('orders/', views.Orders.as_view(), name='order_list'),
    path('orders/<int:pk>', views.OrderDetailView.as_view(), name='order_detail'),
    path('create_order_item/<int:pk>', views.CreateOrderItem.as_view(), name='create_order_detail'),
    path('delete_order_item/<int:pk>', views.delete_order_detail, name='delete_order_item'),
    path('confirm_order/<int:pk>', views.confirm_order, name='confirm_order'),
    path('cancel_order/<int:pk>', views.cancel_order, name='cancel_order'),
]

