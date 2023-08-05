from django.urls import path, include
from . import views

urlpatterns = [
    path('staff_login/', views.StaffLogin.as_view(), name='login'),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('verify/', views.verify, name="verify"),
    path('logout/', views.logout_view, name="logout"),
]