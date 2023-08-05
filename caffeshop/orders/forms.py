from django import forms

class ReserveForm(forms.Form):
    error_css_class = "error"
    required_css_class = "required"
    table_number = forms.IntegerField(max_value=15, min_value=1, widget=forms.NumberInput(attrs={"id":"select-box"}))
    phone = forms.CharField(max_length=11, widget= forms.TextInput(attrs={"id": "phone-input"}), required=True)