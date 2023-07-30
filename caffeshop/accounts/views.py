from django.shortcuts import render, redirect
from .form import StaffLoginForm, VerifyCodeForm
from django.contrib.auth import login
from .authentication import PhoneAuthBackend
from .models import User
from django.contrib import messages


# Create your views here.


def staff_login(request):
    message = None
    if request.method == "POST":
        form = StaffLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = PhoneAuthBackend().authenticate(request, phone=cd["phone"], password=cd["password"])
            if user is not None:
                request.session["phone"] = cd["phone"]
                return redirect("verify")
            else:
                message = "Invalid phone number or password"

    elif request.method == "GET":
        if request.user.is_authenticated:
            return redirect("dashboard")
    form = StaffLoginForm()
    return render(request, "login.html", {"message": message, "form": form})


def verify(request):
    if request.method == "POST":
        form = VerifyCodeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            code = cd["code"]
            phone = request.session["staff_login_info"]["phone"]
            code_instance = Otp_code.objects.filter(phone=phone)

            if code_instance:
                code_instance = code_instance.get(phone=phone)
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
