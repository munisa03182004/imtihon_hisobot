from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()

class UserRegistrationForm(ModelForm):
    
    password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={
        'class': 'p-2 border border-slate-500 rounded w-full',
    }), label="Password")
    password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={
        'class': 'p-2 border border-slate-500 rounded w-full',
    }), label="Confirm Password")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',  'password1', 'password2']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'p-2 border border-slate-500 rounded w-full'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'p-2 border border-slate-500 rounded w-full'
            }),
            'username': forms.TextInput(attrs={
            'class': 'p-2 border border-slate-500 rounded w-full'
            })
        }
