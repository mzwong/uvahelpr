from django import forms
from django.contrib.admin import widgets

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    next = forms.CharField(max_length=100)

class CreateListingForm(forms.Form):
    title = forms.CharField(label='Title', max_length=64)
    description = forms.CharField(label='Description', max_length=64)
    skills_required = forms.CharField(label='Skills Required', max_length=64)
    compensation = forms.DecimalField(label='Compensation')
    event_time = forms.DateTimeField()
    location = forms.CharField(label='Location', max_length=50)
    time_required = forms.DecimalField(label='Time Required')

class CreateAccountForm(forms.Form):
    username = forms.CharField(label='Username', max_length=32)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', max_length=32, widget=forms.PasswordInput)
    first_name = forms.CharField(label='First Name', max_length=32)
    last_name = forms.CharField(label='Last Name', max_length=32)
    phone_number = forms.RegexField(label='Phone Number', regex=r'^\+?1?\d{9,15}$', max_length=17)
    skills = forms.CharField(label='Skills', max_length=1000, required=False)
