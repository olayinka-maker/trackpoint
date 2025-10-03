from django import forms
from django.contrib.auth.models import User
from .models import Staff, Asset, AssetType, Department


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']


class StaffForm(forms.ModelForm):

    class Meta:
        model = Staff
        fields = ['email', 'department', 'position', 'hire_date']


class AssetForm(forms.ModelForm):

    class Meta:
        model = Asset
        fields = [
            'name', 'asset_type', 'department', 'status', 'location',
            'purchase_date'
        ]
