from django.shortcuts import render
import urllib.request
import urllib.parse
import json
from .forms import LoginForm, CreateAccountForm
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
		return render(request, 'marketplace/login.html', {'form': form, 'error':True, 'resp': resp})
	# logged them in. set their login cookie and redirect to back to wherever they came from
	authenticator = resp['result']['authenticator']
	response = HttpResponseRedirect(next)
	response.set_cookie("auth", authenticator["authenticator"])
	return response


def job_entry(request, id):
	# make a GET request and parse the returned JSON                                                                                                                                                           # note, no timeouts, error handling or all the other things needed to do this for real
	#req = urllib.request.Request('http://www.mocky.io/v2/57f001943d0000dc1e0dd7ca')
	req = urllib.request.Request('http://exp-api:8000/jobs/' + id + '/')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
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
	 # created account, redirect to success page
	return HttpResponseRedirect(reverse('create_account_success'))

def create_account_success(request):
	return render(request, 'marketplace/create_account_success.html')