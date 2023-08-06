from django import forms
from .models import Table


class OrderForm(forms.Form):
    error_css_class = "error"
    required_css_class = "required"
    table_number = forms.IntegerField(max_value=len(Table.objects.all()), min_value=1, widget=forms.NumberInput(attrs={"id": "checkbox"}))
    phone = forms.CharField(max_length=11, widget=forms.TextInput(attrs={"id": "phone-input"}), required=True)
