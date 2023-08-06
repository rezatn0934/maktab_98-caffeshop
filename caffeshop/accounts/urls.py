from django.urls import path, include
from . import views

urlpatterns = [
    path('staff_login/', views.StaffLogin.as_view(), name='login'),
    path('dashboard/', views.Dashboard.as_view, name="dashboard"),
    path('verify/', views.Verify.as_view(), name="verify"),
    path('logout/', views.logout_view, name="logout"),
]