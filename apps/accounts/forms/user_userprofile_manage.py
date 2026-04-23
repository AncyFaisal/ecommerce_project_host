import re
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from apps.sanjeri_models import CustomUser

ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/webp']
MAX_IMAGE_SIZE_MB = 2


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone', 'gender', 'address', 'profile_image']
        widgets = {
            'first_name':     forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name', 'maxlength': '150'}),
            'last_name':      forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name', 'maxlength': '150'}),
            'phone':          forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit mobile number', 'maxlength': '10'}),
            'gender':         forms.Select(attrs={'class': 'form-control'}),
            'address':        forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Your address (optional)'}),
            'profile_image':  forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/jpeg,image/png,image/webp'}),
        }

    # ── First Name ───────────────────────────────────────────────────────────
    def clean_first_name(self):
        name = self.cleaned_data.get('first_name', '').strip()
        if not name:
            raise ValidationError("First name is required.")
        if len(name) < 2:
            raise ValidationError("First name must be at least 2 characters.")
        if not re.match(r"^[a-zA-Z\s\-']+$", name):
            raise ValidationError("First name can only contain letters, spaces, hyphens, and apostrophes.")
        return name.strip()

    # ── Last Name ────────────────────────────────────────────────────────────
    def clean_last_name(self):
        name = self.cleaned_data.get('last_name', '').strip()
        if name and not re.match(r"^[a-zA-Z\s\-']+$", name):
            raise ValidationError("Last name can only contain letters, spaces, hyphens, and apostrophes.")
        return name.strip()

    # ── Phone ────────────────────────────────────────────────────────────────
    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not phone:
            return phone  # phone is optional on profile
        if not phone.isdigit():
            raise ValidationError("Phone number must contain digits only.")
        if len(phone) != 10:
            raise ValidationError("Phone number must be exactly 10 digits.")
        if not re.match(r'^[6-9]\d{9}$', phone):
            raise ValidationError("Enter a valid Indian mobile number starting with 6, 7, 8, or 9.")
        return phone

    # ── Profile Image ────────────────────────────────────────────────────────
    def clean_profile_image(self):
        image = self.cleaned_data.get('profile_image')
        if not image or not hasattr(image, 'content_type'):
            return image  # no new upload
        if image.content_type not in ALLOWED_IMAGE_TYPES:
            raise ValidationError("Only JPEG, PNG, and WebP images are allowed.")
        if image.size > MAX_IMAGE_SIZE_MB * 1024 * 1024:
            raise ValidationError(f"Image size must not exceed {MAX_IMAGE_SIZE_MB} MB.")
        return image


class EmailChangeForm(forms.Form):
    new_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter new email address'})
    )
    confirm_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new email address'})
    )
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your current password'})
    )

    def clean_new_email(self):
        email = self.cleaned_data.get('new_email', '').strip().lower()
        if not email:
            raise ValidationError("New email is required.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        new_email = cleaned_data.get('new_email')
        confirm_email = cleaned_data.get('confirm_email', '').strip().lower()
        if new_email and confirm_email and new_email != confirm_email:
            raise ValidationError("Email addresses don't match.")
        return cleaned_data


class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Current password'})
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New password'}),
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password'})
    )

    def clean_new_password(self):
        password = self.cleaned_data.get('new_password', '')
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'\d', password):
            raise ValidationError("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*()\-_,.?":{}|<>]', password):
            raise ValidationError("Password must contain at least one special character.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        if new_password and confirm_password and new_password != confirm_password:
            raise ValidationError("Passwords don't match.")
        return cleaned_data