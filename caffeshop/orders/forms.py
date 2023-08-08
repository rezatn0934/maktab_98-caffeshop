from django import forms
from .models import Order, Table


class OrderForm(forms.ModelForm):
    table_number = forms.ModelChoiceField(queryset=Table.objects.filter(occupied=False), required=False)

    class Meta:
        model = Order
        fields = ["phone_number", "table_number"]