from django import forms
from .models import Order, Table


class OrderForm(forms.ModelForm):
    error_css_class = "error"
    required_css_class = "required"
    table_number = forms.ModelChoiceField(queryset=Table.objects.filter(occupied=False))

    class Meta:
        model = Order
        fields = ["phone_number"]
