from django import forms

class ReserveForm(forms.Form):
    CHOICES = (
    (1,'Indoor'),
    (0,'Outdoor'))
    error_css_class = "error"
    required_css_class = "required"
    # delivery_choice = forms.RadioSelect(choices=CHOICES)
    table_number = forms.IntegerField(max_value=15, min_value=1, widget=forms.NumberInput(attrs={"id":"select-box"}))
    # reserve_date = forms.DateField(widget= forms.DateInput)
    phone = forms.CharField(max_length=11, widget= forms.TextInput(attrs={"id": "phone-input"}), required=True)