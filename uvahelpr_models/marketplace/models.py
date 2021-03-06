from django.db import models
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


class HelprUser(models.Model):
	username = models.CharField(max_length=128, unique=True)
	email = models.CharField(max_length=128, unique=True) #TODO: use a regex?
	password = models.CharField(max_length=128)
	first_name = models.CharField(max_length=128)
	last_name = models.CharField(max_length=128)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
	reputation = models.IntegerField(blank=True, null=True)
	skills = models.CharField(max_length=1000, blank=True)

	updateable_fields = ['username','email','password','first_name','last_name' ,'phone_number', 'reputation', 'skills']

	def __str__(self):
		return "Profile for {}".format(self.first_name+", "+self.last_name)


class Job(models.Model):
	skills_required = models.CharField(max_length=1000) # store array as a JSON string
	requester = models.ForeignKey(HelprUser, related_name='requester')
	servicer = models.ForeignKey(HelprUser, related_name='servicer', blank=True, null=True)
	compensation = models.DecimalField(decimal_places=2, max_digits=10)
	event_time = models.DateTimeField()
	location = models.CharField(max_length=200) # TODO: Change to Address class in the future
	time_required = models.DecimalField(decimal_places=2, max_digits=10)
	title = models.CharField(max_length=200)
	description = models.TextField(max_length=500)

class Message(models.Model):
	sender = models.ForeignKey(HelprUser, related_name='sender')
	recipient = models.ForeignKey(HelprUser, related_name='recipient')
	text_body = models.TextField()
	time_sent = models.DateTimeField()

class Authenticator(models.Model):
	authenticator = models.CharField(primary_key=True, max_length=255)
	auth_user = models.ForeignKey(HelprUser, related_name='auth_user')
	time_created = models.DateTimeField(auto_now_add=True)
