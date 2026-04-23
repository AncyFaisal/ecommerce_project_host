from django import forms
from apps.sanjeri_models import UserData

class UserDataForms(forms.ModelForm):
    class Meta:
        model=UserData
        fields=['name','email']