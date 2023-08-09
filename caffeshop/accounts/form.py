from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from orders.models import Order_detail


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('phone', 'first_name', 'last_name', "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('phone', 'first_name', 'last_name')


class StaffLoginForm(forms.Form):
    phone = forms.RegexField(regex=r"^09\d{9}$",
                             widget=forms.TextInput(attrs={
                                 'placeholder': 'Phone number Should Start with 09'}))


class VerifyCodeForm(forms.Form):
    otp_code = forms.RegexField(regex=r"^\d{6}$")


class OrderDetailUpdateForm(forms.ModelForm):
    class Meta:
        model = Order_detail
        fields = ['product', 'quantity']
