from django import forms
from .models import PresentationData
import re
from datetime import date

CONSTITUENCIES_BY_DISTRICT = {
    "Srikakulam": ["Ichchapuram", "Palasa", "Tekkali", "Pathapatnam", "Srikakulam", "Amadalavalasa", "Etcherla", "Narasannapeta"],
    "Vizianagaram": ["Rajam", "Palakonda", "Kurupam", "Parvathipuram", "Salur", "Bobbili", "Cheepurupalli", "Gajapathinagaram", "Nellimarla", "Vizianagaram"],
    "Parvathipuram Manyam": ["Kurupam", "Parvathipuram", "Salur", "Araku Valley"],
    "Visakhapatnam": ["Srungavarapukota", "Bhimili", "Visakhapatnam East", "Visakhapatnam South", "Visakhapatnam North", "Visakhapatnam West", "Gajuwaka", "Chodavaram", "Elamanchili", "Pendurthi"],
    "Anakapalli": ["Madugula", "Anakapalle", "Pendurthi", "Payakaraopet", "Tuni", "Narsipatnam", "Chodavaram", "Pendurthi"],
    "Alluri Sitharama Raju": ["Araku Valley", "Paderu", "Rampachodravaram"],
    "Kakinada": ["Tuni", "Prathipadu", "Pithapuram", "Kakinada Rural", "Kakinada City", "Ramachandrapuram", "Mummidivaram"],
    "East Godavari": ["Anaparthy", "Kakinada City", "Ramachandrapuram", "Mummidivaram", "Razole", "Kothapeta", "Mandapeta"],
    "Konaseema": ["Amalapuram", "Razole", "Mummidivaram", "Kothapeta", "Ramachandrapuram", "Mummidivaram", "Kothapeta"],
    "West Godavari": ["Achanta", "Palakollu", "Bhimavaram", "Undi", "Tanuku", "Tadepalligudem", "Unguturu"],
    "Eluru": ["Unguturu", "Denduluru", "Polavaram", "Chintalapudi", "Tiruvuru", "Nuzvid", "Kaikalur"],
    "NTR": ["Nuzvid", "Gannavaram", "Kaikalur", "Pedana", "Machilipatnam", "Avanigadda", "Pamarru"],
    "Krishna": ["Gannavaram", "Gudivada", "Kaikalur", "Pedana", "Machilipatnam", "Avanigadda", "Pamarru"],
    "Guntur": ["Pedakurapadu", "Tadikonda", "Mangalagiri", "Ponnuru", "Vemuru", "Repalle", "Tenali"],
    "Palnadu": ["Chilakaluripet", "Narasaraopet", "Sattenapalle", "Vinukonda", "Gurazala", "Macherla", "Yerragondapalem"],
    "Bapatla": ["Darsi", "Parchur", "Addanki", "Chirala", "Santhanuthalapadu", "Ongole", "Markapuram"],
    "Prakasam": ["Yerragondapalem", "Darsi", "Parchur", "Addanki", "Chirala", "Santhanuthalapadu", "Ongole", "Kandukur", "Markapuram"],
    "Nellore": ["Kondapi", "Kavali", "Atmakur", "Nellore City", "Nellore Rural", "Udayagiri"],
    "Tirupati": ["Kavali", "Gudur", "Sullurpeta", "Nagari", "Tirupati", "Srikalahasti"],
    "Chittoor": ["Punganur", "Chandragiri", "Tirupati", "Satyavedu", "Nagari", "Chittoor", "Puthalapattu", "Palamaner", "Kuppam"],
    "Annamayya": ["Rajampet", "Kodur", "Rayachoti", "Thamballapalle", "Pileru", "Madanapalle"],
    "YSR Kadapa": ["Badvel", "Kadapa", "Rayachoti", "Pulivendla", "Kamalapuram", "Jammalamadugu", "Proddatur", "Mydukur"],
    "Nandyal": ["Allagadda", "Nandyal", "Nandikotkur", "Banaganapalle", "Dhone", "Pattikonda"],
    "Kurnool": ["Kurnool", "Pattikonda", "Adoni", "Alur", "Kodumur", "Yemmiganur", "Mantralayam"],
    "Ananthapuramu": ["Rayadurg", "Uravakonda", "Guntakal", "Tadipatri", "Singanamala", "Anantapur Urban", "Kalyandurg", "Hindupur"],
    "Sri Sathya Sai": ["Madakasira", "Hindupur", "Penukonda", "Puttaparthi", "Dharmavaram", "Kadiri"]
}

DISTRICT_CHOICES = [(d, d) for d in CONSTITUENCIES_BY_DISTRICT.keys()]

class PresentationForm(forms.ModelForm):
    ap = forms.CharField(label='AP (ap1 and ap2)', max_length=200)
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'required': True}),
        initial=date.today,
        input_formats=["%Y-%m-%d"],
    )

    ap_district = forms.ChoiceField(
        choices=[('', 'Select District')] + DISTRICT_CHOICES,
        required=True, label="AP District"
    )
    ap_constitution = forms.ChoiceField(
        choices=[('', 'Select Constitution')],
        required=True, label="AP Constitution"
    )
    address = forms.CharField(
        label='Address',
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter address here',
            'rows': 4,
            'cols': 40
        })
    )

    class Meta:
        model = PresentationData
        fields = ['date', 'toname', 'phno', 'aadharno', 'ap', 'aptdas', 'ap_district', 'ap_constitution', 'address']
        widgets = {
            'toname': forms.TextInput(attrs={'required': True}),
            'phno': forms.TextInput(attrs={'required': True}),
            'aadharno': forms.TextInput(attrs={'required': True}),
            'ap': forms.TextInput(attrs={'required': True}),
            'aptdas': forms.TextInput(attrs={'required': True}),
        }

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