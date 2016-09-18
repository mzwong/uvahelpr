from django.contrib.auth.models import User
from .models import Profile
from django.forms.models import ModelForm

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'skills']


