from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from json import dumps
from django.forms.models import model_to_dict

from .forms import UserForm, ProfileForm, JobForm, MessageForm
from .models import Profile, Job, Message

############ VIEWS ####################

######### Function-based #############

# Creating a user
@require_http_methods(["POST"])
def create_user(request):
	result = {}
	user_form = UserForm(request.POST)
	profile_form = ProfileForm(request.POST)
	if user_form.is_valid() and profile_form.is_valid():
		user = user_form.save()
		profile = profile_form.save(commit=False)
		profile.user = user
		profile.save()
		result["ok"] = True
		result["result"] = {"id": user.id}
	else:
		result["ok"] = False
		result["result"] = "Invalid form data."
		result["submitted_data"] = dumps(request.POST)
	return JsonResponse(result)

#Deleting a user
@require_http_methods(["POST"])
def delete_user(request):
	result = {}
	try:
		user = User.objects.get(pk=request.POST["id"])
		user.delete()
		result["ok"] = True
		result["result"] = "User succesfully deleted."
	except ObjectDoesNotExist:
		result["ok"] = False
		result["result"] = "User does not exist."
	return JsonResponse(result)

#getting all jobs
@require_http_methods(["GET"])
def get_all_jobs(request):
	result = {}
	try:
		result["ok"] = True
		result["result"] = [model_to_dict(job) for job in Job.objects.all()]
	except Exception:
		result["ok"] = False
		result["result"] = []
	return JsonResponse(result)

#Creating a job
@require_http_methods(["POST"])
def create_job(request):
	result = {}
	job_form = JobForm(request.POST)
	if job_form.is_valid():
		job = job_form.save()
		job.save()
		result["ok"] = True
		result["result"] = {"id": job.id}
	else:
		result["ok"] = False
		result["result"] = "Invalid form data."
		result["submitted_data"] = dumps(request.POST)
	return JsonResponse(result)

#Deleting a job
@require_http_methods(["POST"])
def delete_job(request):
	result = {}
	try:
		job = Job.objects.get(pk=request.POST["id"])
		job.delete()
		result["ok"] = True
		result["result"] = "Job succesfully deleted."
	except ObjectDoesNotExist:
		result["ok"] = False
		result["result"] = "Job does not exist."
	return JsonResponse(result)

#Creating a message
@require_http_methods(["POST"])
def create_message(request):
	result = {}
	message_form = MessageForm(request.POST)
	if message_form.is_valid():
		message = message_form.save()
		message.save()
		result["ok"] = True
		result["result"] = {"id": message.id}
	else:
		result["ok"] = False
		result["result"] = "Invalid form data."
		result["submitted_data"] = dumps(request.POST)
	return JsonResponse(result)

#Deleting a message
@require_http_methods(["POST"])
def delete_message(request):
	result = {}
	try:
		message = Message.objects.get(pk=request.POST["id"])
		message.delete()
		result["ok"] = True
		result["result"] = "Message succesfully deleted."
	except ObjectDoesNotExist:
		result["ok"] = False
		result["result"] = "Message does not exist."
	return JsonResponse(result)

########## Class-based #######################

# Retrieving/updating a user instance
class UserRU(View):

	def get(self, request, id):
		result = {}
		try:
			user = User.objects.get(pk=id)
			result["ok"] = True
			attr_dict = model_to_dict(user, fields=('id', 'username', 'email', 'first_name', 'last_name'))
			attr_dict.update(model_to_dict(user.profile, fields=Profile.updateable_fields))
			result["result"] = dumps(attr_dict)
		except ObjectDoesNotExist:
			result["ok"] = False
			result["result"] = "User does not exist."
		return JsonResponse(result)

	def post(self, request, id):
		result = {}
		try:
			user = User.objects.get(pk=id)
			user_fields = [f.name for f in User._meta.get_fields()]
			for field in user_fields:
				if field in request.POST:
					setattr(user, field, request.POST[field])
			for field in Profile.updateable_fields:
				if field in request.POST:
					setattr(user.profile, field, request.POST[field])
			user.save()
			user.profile.save()
			result["ok"] = True
			result["result"] = "User updated succesfully."
		except ObjectDoesNotExist:
			result["ok"] = False
			result["result"] = "User does not exist."
		return JsonResponse(result)

class JobRU(View):
	def get(self, request, id):
		result = {}
		try:
			job = Job.objects.get(pk=id)
			result["ok"] = True
			result["result"] = model_to_dict(job)
		except ObjectDoesNotExist:
			result["ok"] = False
			result["result"] = "Job does not exist."
		return JsonResponse(result)

	def post(self, request, id):
		result = {}
		try:
			job = Job.objects.get(pk=id)
			job_fields = [f.name for f in Job._meta.get_fields()]
			for field in job_fields:
				if field in request.POST:
					setattr(job, field, request.POST[field])
			job.save()
			result["ok"] = True
			result["result"] = "Job updated succesfully."
		except ObjectDoesNotExist:
			result["ok"] = False
			result["result"] = "Job does not exist."
		return JsonResponse(result)

class MessageRU(View):
	def get(self, request, id):
		result = {}
		try:
			message = Message.objects.get(pk=id)
			result["ok"] = True
			result["result"] = model_to_dict(message);
		except ObjectDoesNotExist:
			result["ok"] = False
			result["result"] = "Message does not exist."
		return JsonResponse(result)

	def post(self, request, id):
		result = {}
		try:
			message = Message.objects.get(pk=id)
			message_fields = [f.name for f in Message._meta.get_fields()]
			for field in message_fields:
				if field in request.POST:
					setattr(message, field, request.POST[field])
			message.save()
			result["ok"] = True
			result["result"] = "Message updated succesfully."
		except ObjectDoesNotExist:
			result["ok"] = False
			result["result"] = "Message does not exist."
		return JsonResponse(result)