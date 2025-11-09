from django import forms
from .models import PresentationData
import re
from datetime import date



class PresentationForm(forms.ModelForm):
    ap = forms.CharField(label='AP (ap1 and ap2)', max_length=200)
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',       # uses browser's date picker
            'required': True
        }),
        initial=date.today,        # sets the default value to today's date
        input_formats=["%Y-%m-%d"]
    )
    
    class Meta:
        model = PresentationData
        fields = ['date', 'toname', 'phno', 'aadharno', 'ap', 'aptdas']
        widgets = {
            'toname': forms.TextInput(attrs={'required': True}),
            'phno': forms.TextInput(attrs={'required': True}),
            'aadharno': forms.TextInput(attrs={'required': True}),
            'ap': forms.TextInput(attrs={'required': True}),
            'aptdas': forms.TextInput(attrs={'required': True}),
        }
    # (Your custom validators remain the same)

    def clean_phno(self):
        phno = self.cleaned_data.get('phno', '')
        if not re.fullmatch(r'\d{10}', phno):
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        return phno

    def clean_aadharno(self):
        aadharno = self.cleaned_data.get('aadharno', '')
        if not re.fullmatch(r'\d{12}', aadharno):
            raise forms.ValidationError("Aadhar number must be exactly 12 digits.")
        return aadharno

    def clean(self):
        cleaned_data = super().clean()
        ap = cleaned_data.get("ap", "")
        parts = ap.split(' ', 1)
        cleaned_data['ap1'] = parts[0]
        cleaned_data['ap2'] = parts[1] if len(parts) > 1 else ''
        return cleaned_data
