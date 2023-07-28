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
                random_code = random.randint(10000000, 99999999)
                send_otp_code(cd["phone"], random_code)
                Otp_code.objects.create(phone=cd["phone"], code=random_code)

                request.session["staff_login_info"] = {
                    "phone": cd["phone"],
                }

                messages.success(request, "8-digit code was sent for you", 'success')
                return redirect("verify")
            else:

                messages.error(request, "username and password are wrong", "danger")
                return redirect("login")

    elif request.method == "GET":
        form = StaffLoginForm()

    return render(request, "login.html", {"form": form})


def verify(request):
    if request.method == "POST":
        form = VerifyCodeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            code = cd["code"]
            phone = request.session["staff_login_info"]["phone"]
            code_instance = Otp_code.objects.get(phone=phone)

            if code_instance:
                if int(code) == code_instance.code:
                    Otp_code.objects.filter(phone=phone).delete()
                    user = User.objects.get(phone=phone)
                    login(request, user, backend='accounts.authentication.PhoneAuthBackend')
                    messages.success(request, "logged in successfully", "success")
                    return redirect("dashboard")
                else:
                    messages.success(request, "code is wrong", "danger")
                    return redirect("verify")
            else:
                messages.success(request, "Your code has been expired", "danger")
                return redirect("login")

    else:
        form = VerifyCodeForm()
    return render(request, "verify.html", {"form": form})


def dashboard(request):
    return render(request, "dashboard.html")
