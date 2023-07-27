from django.urls import path
from . import views

urlpatterns = [
    path('admin_login/', views.create_admin, name='admin')
]