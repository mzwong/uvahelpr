from django.shortcuts import render, redirect
import urllib.request
import urllib.parse
from urllib.error import HTTPError
import json
from .forms import LoginForm
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
		return render(request, 'marketplace/login.html', {'form': form, 'error':True})
	# logged them in. set their login cookie and redirect to back to wherever they came from
	authenticator = resp['result']['authenticator']
	response = HttpResponseRedirect(next)
	response.set_cookie("auth", authenticator["authenticator"])
	return response

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



