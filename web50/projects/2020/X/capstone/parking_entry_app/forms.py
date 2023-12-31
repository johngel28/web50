# parking_entry_app/forms.py
from django import forms

class TransactionSearchForm(forms.Form):
    plate_number = forms.CharField(required=False)
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    status = forms.ChoiceField(choices=[('', 'Select Status'), ('IN', 'IN'), ('OUT', 'OUT')], required=False)
