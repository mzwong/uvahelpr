from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from json import dumps
from django.forms.models import model_to_dict

from .forms import UserForm, ProfileForm
from .models import Profile

############ VIEWS ####################

######### Function-based #############
def index(request):
	return render(request, 'marketplace/index.html')


# Creating a user
@require_http_methods(["POST"])
def create_user(request):
	result = {}
	user_form = UserForm(request.POST)
	profile_form = ProfileForm(request.POST)
	if user_form.is_valid() and profile_form.is_valid():
		user = user_form.save()
		profile = profile_form.save()
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

