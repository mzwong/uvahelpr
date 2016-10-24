from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

class CreateAccountForm(forms.Form):
    username = forms.CharField(label='Username', max_length=32)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', max_length=32, widget=forms.PasswordInput)
    first_name = forms.CharField(label='First Name', max_length=32)
    last_name = forms.CharField(label='Last Name', max_length=32)
    phone_number = forms.RegexField(label='Phone Number', regex=r'^\+?1?\d{9,15}$', max_length=17)
    skills = forms.CharField(label='Skills', max_length=1000, required=False)
