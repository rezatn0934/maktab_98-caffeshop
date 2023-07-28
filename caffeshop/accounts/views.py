from django.shortcuts import render, redirect
from .form import StaffLoginForm, VerifyCodeForm
from django.contrib.auth import login
from .authentication import PhoneAuthBackend
import random
from utils import send_otp_code
from .models import Otp_code, User
from django.contrib import messages


# Create your views here.


def staff_login(request):
    if request.method == "POST":
        form = StaffLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = PhoneAuthBackend().authenticate(request, phone=cd["phone"], password=cd["password"])
            if user is not None:
                random_code = random.randint(1000, 9999)
                send_otp_code(cd["phone"], random_code)
                Otp_code.objects.create(phone=cd["phone"], code=random_code)

                request.session["staff_login_info"] = {
                    "phone": cd["phone"],
                }

                messages.success(request, "6-digit code was sent for you", 'success')
                return redirect("verify")
            else:

                messages.error(request, "username and password are wrong", "danger")
                return redirect("login")

    elif request.method == "GET":
        form = StaffLoginForm()

    return render(request, "login.html", {"form": form})
