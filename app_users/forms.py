from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()

class UserRegistrationForm(ModelForm):
    """
    Form for user registration.

    This form extends Django's ModelForm and is used for registering new users.
    It includes fields for first name, last name, username, password, and password confirmation.

    Attributes:
        password1 (CharField): Field for entering the password.
        password2 (CharField): Field for confirming the password.

    Meta:
        model (User): The user model for which the form is created.
        fields (list): List of fields to include in the form.
        widgets (dict): Dictionary containing custom widgets for form fields.
    """

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
