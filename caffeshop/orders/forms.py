from django import forms

class ReserveForm(forms.Form):
    CHOICES = (
    (1,'Indoor'),
    (0,'Outdoor'))
    error_css_class = "error"
    required_css_class = "required"
    table_number = forms.IntegerField(max_value=15, min_value=1, attrs={"class":"", "id":"select-box"}, label="Table No")
    reserve_date = forms.DateTimeField(widget= forms.DateTimeInput, label="Reserve Date")
    phone = forms.CharField(max_length=11, widget= forms.TextInput(attrs={"id": "phone-input"}), required=True, label="Phone nuber")
    delivery_choice = forms.RadioSelect(choices=CHOICES, widget=forms.RadioSelect, attrs={"class":"", "id":"select-box"})