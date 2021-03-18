
from .models import *
from django import forms
from django.contrib.auth.forms import *


class RegisterForm(forms.ModelForm):

    class Meta:
        model = Staff
        fields = ['email', 'fname', 'lname', 'passwrd', 'img']
        widgets = {}

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Email'})
        self.fields['fname'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'First Name'})
        self.fields['lname'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Last name'})
        self.fields['passwrd'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'})
