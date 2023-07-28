from django.urls import path
from . import views

urlpatterns = [
    path('staff_login/', views.staff_login, name='login'),
    path('dashboard/', views.dashboard, name="dashboard"),

]