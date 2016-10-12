from .models import HelprUser, Job, Message
from django.forms.models import ModelForm

# class UserForm(ModelForm):
#     class Meta:
#         model = User
#         fields = []

class HelprUserForm(ModelForm):
    class Meta:
        model = HelprUser
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'phone_number', 'skills']

class JobForm(ModelForm):
	class Meta:
		model = Job
		fields = ['skills_required','requester_id', 'servicer_id', 'compensation', 'event_time', 'location','time_required']

class MessageForm(ModelForm):
	class Meta:
		model = Message
		fields = ['sender_id', 'recipient_id', 'text_body', 'time_sent']
