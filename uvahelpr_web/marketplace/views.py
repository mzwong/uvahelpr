from django.shortcuts import render, redirect
import urllib.request
import urllib.parse
from urllib.error import HTTPError
import json
from .forms import LoginForm, CreateAccountForm, CreateListingForm
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
# Create your views here.
def index(request):
	return render(request, 'marketplace/index.html')

def login(request):
	if request.method == 'GET':
		form = LoginForm()
		next = request.GET.get('next') or reverse('index')
		return render(request, 'marketplace/login.html', {'form': form})
	form = LoginForm(request.POST)
	# check whether it's valid:
	if not form.is_valid():
		return render(request, 'marketplace/login.html', {'form': form})
	email = form.cleaned_data['email']
	password = form.cleaned_data['password']
	next = form.cleaned_data.get('next') or reverse('index')
	post_data = {'email': email, 'password': password}
	post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
	req = urllib.request.Request('http://exp-api:8000/login/', data=post_encoded, method='POST')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	if not resp or not resp['ok']:
		# couldn't log them in, send them back to login page with error
		return render(request, 'marketplace/login.html', {'form': form, 'error': True})
	# logged them in. set their login cookie and redirect to back to wherever they came from
	authenticator = resp['result']['authenticator']
	response = HttpResponseRedirect(next)
	response.set_cookie("auth", authenticator["authenticator"])
	return response

def create_listing(request):
	form = CreateListingForm(request.POST)
	if request.method == 'GET':
		return render(request, "marketplace/create_listing.html", {'form': form})
	auth = request.COOKIES.get('auth');
	if not auth:
		#Handle user not logged in while trying to create a listing
		return HttpResponseRedirect(reverse("login") + "?next=" + reverse("create_listing"))
	if not form.is_valid():
		return render(request, 'marketplace/create_listing.html', {'form': form})
	skills = form.cleaned_data['skills']
	requester = form.cleaned_data['requester']
	compensation = form.cleaned_data['compensation']
	time = form.cleaned_data['time']
	location = form.cleaned_data['location']
	duration = form.cleaned_data['duration']
	post_data = {'skills': skills,
				 'requester': requester,
				 'compensation': compensation,
				 'time': time,
				 'location': location,
				 'duration': duration}
	post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
	req = urllib.request.Request('http://exp-api:8000/create_job/', data=post_encoded, method='POST')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	#if resp and not resp['ok']:
		# exp service reports invalid authenticator -- treat like user not logged in
	#	return HttpResponseRedirect(reverse("login") + "?next=" + reverse("create_listing"))
	if not resp or not resp['ok']:
		# couldn't create lsiting, send them back to create listing page with error
		return render(request, 'marketplace/create_listing.html', {'form': form, 'error': True})
	# successfully created listing
	authenticator = resp['result']['authenticator']
	return render(request, 'marketplace/create_listing_success.html')

def create_listing_success(request):
	return render(request, 'marketplace/create_listing_success.html')

def logout(request):
	authkey = request.COOKIES.get('auth')
	if authkey is not None:
		post_data = {'auth': authkey}
		post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
		req = urllib.request.Request('http://exp-api:8000/logout/', data=post_encoded, method='POST')
		urllib.request.urlopen(req).read().decode('utf-8')
	response = HttpResponseRedirect('/market/')
	response.delete_cookie('auth')
	return response

def job_entry(request, id):
	# make a GET request and parse the returned JSON
	req = urllib.request.Request('http://exp-api:8000/jobs/' + id + '/')
	#redirect to all jobs view if job cannot be accessed/does not exist
	try:
		resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	except HTTPError:
		return redirect('allJobs')
	resp_dict = json.loads(resp_json)
	context = {"job": resp_dict['result']}
	return render(request, 'marketplace/job_detail.html', context=context)

def allJobs(request):
	#Experience service call to get all jobs
	req = urllib.request.Request('http://exp-api:8000/jobs/')

	#mock response data for testing:
	#req = urllib.request.Request('http://www.mocky.io/v2/57efed1a3d0000371e0dd7c4')

	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	context = {'job_list' : resp['result']}
	return render(request, 'marketplace/jobslist.html', context)

def create_account(request):
	if request.method == 'GET':
		form = CreateAccountForm()
		return render(request, 'marketplace/create_account.html', {'form': form})
	form = CreateAccountForm(request.POST)
	# check whether it's valid:
	if not form.is_valid():
	 	return render(request, 'marketplace/create_account.html', {'form': form})
	username = form.cleaned_data['username']
	email = form.cleaned_data['email']
	password = form.cleaned_data['password']
	first_name = form.cleaned_data['first_name']
	last_name = form.cleaned_data['last_name']
	phone_number = form.cleaned_data['phone_number']
	skills = form.cleaned_data['skills']
	post_data = {'username': username,
				 'email': email,
				 'password': password,
				 'first_name':first_name,
				 'last_name':last_name,
				 'phone_number': phone_number,
				 'skills': skills}
	post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
	req = urllib.request.Request('http://exp-api:8000/create_account/', data=post_encoded, method='POST')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	if not resp or not resp['ok']:
	 	# couldn't create account, send them back to account page with error
	 	return render(request, 'marketplace/create_account.html', {'form': form, 'error':True})
	# created account, log-in, redirect to index
	post_data = {'email': email, 'password': password}
	post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
	req = urllib.request.Request('http://exp-api:8000/login/', data=post_encoded, method='POST')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	authenticator = resp['result']['authenticator']
	response = HttpResponseRedirect(reverse('index'))
	response.set_cookie("auth", authenticator["authenticator"])
	return response
