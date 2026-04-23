# forms/user_address_manage.py
import re
from django import forms
from django.core.exceptions import ValidationError
from apps.sanjeri_models import Address, CustomUser


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'address_type', 'full_name', 'phone',
            'address_line1', 'address_line2', 'city',
            'state', 'postal_code', 'country', 'landmark', 'is_default',
        ]
        widgets = {
            'address_type':  forms.Select(attrs={'class': 'form-control'}),
            'full_name':     forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'phone':         forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit mobile number', 'maxlength': '10'}),
            'address_line1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'House / Flat no., Street, Area'}),
            'address_line2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apartment, Colony (optional)'}),
            'city':          forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state':         forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'postal_code':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': '6-digit PIN code', 'maxlength': '6'}),
            'country':       forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'landmark':      forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nearby landmark (optional)'}),
            'is_default':    forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    # ── Full Name ────────────────────────────────────────────────────────────
    def clean_full_name(self):
        name = self.cleaned_data.get('full_name', '').strip()
        if not name:
            raise ValidationError("Full name is required.")
        if len(name) < 3:
            raise ValidationError("Full name must be at least 3 characters.")
        if len(name) > 100:
            raise ValidationError("Full name cannot exceed 100 characters.")
        if not re.match(r"^[a-zA-Z\s\.\-']+$", name):
            raise ValidationError("Full name can only contain letters, spaces, hyphens, apostrophes, and dots.")
        return name

    # ── Phone ────────────────────────────────────────────────────────────────
    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not phone:
            raise ValidationError("Phone number is required.")
        if not phone.isdigit():
            raise ValidationError("Phone number must contain digits only.")
        if len(phone) != 10:
            raise ValidationError("Phone number must be exactly 10 digits.")
        if not re.match(r'^[6-9]\d{9}$', phone):
            raise ValidationError("Enter a valid Indian mobile number starting with 6, 7, 8, or 9.")
        return phone

    # ── Address Line 1 ───────────────────────────────────────────────────────
    def clean_address_line1(self):
        line1 = self.cleaned_data.get('address_line1', '').strip()
        if not line1:
            raise ValidationError("Address Line 1 is required.")
        if len(line1) > 255:
            raise ValidationError("Address Line 1 cannot exceed 255 characters.")
        return line1

    # ── City ─────────────────────────────────────────────────────────────────
    def clean_city(self):
        city = self.cleaned_data.get('city', '').strip()
        if not city:
            raise ValidationError("City is required.")
        if len(city) < 2:
            raise ValidationError("City name must be at least 2 characters.")
        if not re.match(r"^[a-zA-Z\s\-\.]+$", city):
            raise ValidationError("City name can only contain letters, spaces, hyphens, and dots.")
        return city.title()

    # ── State ────────────────────────────────────────────────────────────────
    def clean_state(self):
        state = self.cleaned_data.get('state', '').strip()
        if not state:
            raise ValidationError("State is required.")
        if len(state) < 2:
            raise ValidationError("State name must be at least 2 characters.")
        if not re.match(r"^[a-zA-Z\s\-\.]+$", state):
            raise ValidationError("State name can only contain letters, spaces, hyphens, and dots.")
        return state.title()

    # ── Postal Code ──────────────────────────────────────────────────────────
    def clean_postal_code(self):
        code = self.cleaned_data.get('postal_code', '').strip()
        if not code:
            raise ValidationError("Postal code is required.")
        if not code.isdigit():
            raise ValidationError("Postal code must contain digits only.")
        if len(code) != 6:
            raise ValidationError("Indian PIN code must be exactly 6 digits.")
        if code[0] == '0':
            raise ValidationError("PIN code cannot start with 0.")
        return code

    # ── Country ──────────────────────────────────────────────────────────────
    def clean_country(self):
        country = self.cleaned_data.get('country', '').strip()
        if not country:
            raise ValidationError("Country is required.")
        if len(country) < 2:
            raise ValidationError("Country name must be at least 2 characters.")
        if not re.match(r"^[a-zA-Z\s\-\.]+$", country):
            raise ValidationError("Country name can only contain letters, spaces, hyphens, and dots.")
        return country.title()