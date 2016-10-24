from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)


class CreateListingForm(forms.Form):
    skills = forms.CharField(label='Skills Required', max_length=64)
    requester = forms.CharField(label='Requester', max_length=140)
    time = forms.CharField(label='Time', max_length=20)
    compensation = forms.CharField(label='Compensation Offered', max_length=20)
    location = forms.CharField(label='Location', max_length=50)
    duration = forms.CharField(label='Duration', max_length=20)


