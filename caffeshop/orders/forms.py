from django import forms
from .models import Order, Table


class OrderForm(forms.ModelForm):
    error_css_class = "error"
    required_css_class = "required"
    table_number = forms.ModelChoiceField(queryset=Table.objects.all())

    # phone = forms.CharField(max_length=11, widget=forms.TextInput(attrs={"id": "phone-input"}), required=True)
    class Meta:
        model = Order
        fields = ["phone_number"]
