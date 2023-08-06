from django.shortcuts import render, redirect
from .form import StaffLoginForm, VerifyCodeForm
from django.contrib.auth import login, logout
from .authentication import PhoneAuthBackend
from .models import User
from utils import send_otp_code
import datetime
from django.utils import timezone
from django.views import View


# Create your views here.

class StaffLogin(View):
    message = None
    form = StaffLoginForm
    html_temp = "login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")
        context = {"message": self.message, "form": self.form()}
        return render(request, self.html_temp, context=context)

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            phone = cd["phone"]
            user = PhoneAuthBackend().authenticate(request, phone=phone)
            if user is not None:
                request.session["phone"] = phone
                return redirect("verify")
            else:
                message = "Invalid phone number"
        else:
            message = "wrong input"

        context = {"message": message, "form": self.form()}
        return render(request, self.html_temp, context=context)


class Verify(View):
    message = None
    form = VerifyCodeForm
    html_temp = "verify.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")
        if request.session.get("phone") is None:
            return redirect("login")

        message = "6-digit code was sent for you, you only have 60 seconds"
        send_otp_code(request, request.session.get("phone"))
        context = {"message": message, "form": self.form()}
        return render(request, self.html_temp, context=context)

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            code = cd["code"]
            phone = request.session["phone"]
            otp_key = request.session.get("otp_code")
            otp_valid_date = request.session.get("otp_valid_date")
            if otp_key is not None and otp_valid_date is not None:
                valid_until = datetime.datetime.fromisoformat(otp_valid_date)
                if valid_until > timezone.now():
                    if code == otp_key:
                        user = User.objects.get(phone=phone)
                        login(request, user, backend='accounts.authentication.PhoneAuthBackend')
                        del request.session["otp_code"]
                        del request.session["otp_valid_date"]
                        return redirect("dashboard")
                    else:
                        message = "Invalid OTP"
                else:
                    message = "OTP has been expired"
            else:
                message = "Start from here!"
        else:
            message = "wrong input"

        form = self.form()
        context = {"message": message, "form": form}
        return render(request, self.html_temp, context=context)


def dashboard(request):
    return render(request, "dashboard.html")


def logout_view(request):
    logout(request)
    return redirect("login")