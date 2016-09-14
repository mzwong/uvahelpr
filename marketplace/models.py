from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class UvaUser(User):
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex], max_length=17) # validators should be a list
	reputation = (
		(5, '5'),
		(4, '4'),
		(3, '3'),
		(2, '2'),
		(1, '1'),
	)
	skills = models.CharField(max_length=1000) # store array as a JSON string

class Job(models.Model):
	requester_id = models.ForeignKey(UvaUser, related_name='requester')
	servicer_id = models.ForeignKey(UvaUser, related_name='servicer')
	compensation = models.DecimalField(decimal_places=2, max_digits=10)
	event_time = models.DateTimeField();
	Location = models.CharField(max_length=200) # TODO: Change to Address class in the future
	time_required = models.DecimalField(decimal_places=2, max_digits=10)
	skills_required = models.CharField(max_length=1000) # store array as a JSON string

class Message(models.Model):
	sender_id = models.ForeignKey(UvaUser, related_name='sender')
	recipient_id = models.ForeignKey(UvaUser, related_name='recipient')
	text_body = models.TextField()
	time_sent = models.TimeField()