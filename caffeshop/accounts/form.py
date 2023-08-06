from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django import forms
import re


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone', 'first_name', 'last_name')

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
    phone = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone")
        if not re.match(r"^09\d{9}$", phone):
            raise forms.ValidationError(" Wrong Input")
        return cleaned_data


class VerifyCodeForm(forms.Form):
    code = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get("code")
        if not re.match(r"^\d{6}$", code):
            raise forms.ValidationError(" Wrong Input")
        return cleaned_data
