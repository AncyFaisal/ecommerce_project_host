# forms/category.py
import re
from django import forms
from django.core.exceptions import ValidationError
from apps.sanjeri_models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name',
                'maxlength': '100',
                'autocomplete': 'off',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category description (optional)',
                'rows': 4,
                'maxlength': '500',
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()

        if not name:
            raise ValidationError("Category name is required.")

        if len(name) < 3:
            raise ValidationError("Category name must be at least 3 characters.")

        if len(name) > 100:
            raise ValidationError("Category name cannot exceed 100 characters.")

        if not re.match(r"^[a-zA-Z0-9]", name):
            raise ValidationError("Category name must start with a letter or number.")

        if not re.match(r"^[a-zA-Z0-9][a-zA-Z0-9\s\-&'().]+$", name):
            raise ValidationError(
                "Only letters, numbers, spaces, hyphens, ampersands, apostrophes, and parentheses are allowed."
            )

        if re.search(r'\s{2,}', name):
            raise ValidationError("Category name cannot contain consecutive spaces.")

        # Duplicate check (case-insensitive), excluding current instance on edit
        qs = Category.objects.filter(name__iexact=name, is_deleted=False)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError(f'A category named "{name}" already exists.')

        return name.strip()

    def clean_description(self):
        desc = self.cleaned_data.get('description', '')
        if desc and len(desc) > 500:
            raise ValidationError("Description cannot exceed 500 characters.")
        return desc
