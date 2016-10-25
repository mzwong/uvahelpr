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
        fields = ['title', 'description', 'skills_required', 'compensation', 'event_time', 'location', 'time_required', 'requester']

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'text_body', 'time_sent']
