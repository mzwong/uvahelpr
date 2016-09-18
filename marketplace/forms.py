from django.contrib.auth.models import User
from .models import Profile, Job
from django.forms.models import ModelForm

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'skills']

class JobForm(ModelForm):
	class Meta:
		model = Job
		fields = ['skills_required','requester_id', 'servicer_id', 'compensation', 'event_time', 'location','time_required']
