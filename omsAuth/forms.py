from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.shortcuts import get_object_or_404



class OMSUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class OMSStaffCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',)
