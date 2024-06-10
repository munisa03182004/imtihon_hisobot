from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Cost


User = get_user_model()


class Cost(ModelForm):
    class Meta:
        model = Cost
        fields = ['amount','transaction_type','name']