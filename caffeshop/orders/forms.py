from django import forms
from .models import Order, Table


class OrderForm(forms.ModelForm):
    table_number = forms.ModelChoiceField(label="Table Name:(if takeaway, skip this)",
                                          queryset=Table.objects.filter(occupied=False),
                                          required=False, widget=forms.Select(
            attrs={'class': 'form-control control-label text-center'}))

    class Meta:
        model = Order
        fields = ["phone_number", "table_number"]

        widgets = {"phone_number": forms.TextInput(
            attrs={"class": "form-control control-label text-center",
                   'placeholder': 'Phone number Should Start with 09'})}
