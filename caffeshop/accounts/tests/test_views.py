from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import User
from accounts.form import CustomUserCreationForm
from accounts.views import (
    StaffLogin,
)


class TestStaffLogin(TestCase):
