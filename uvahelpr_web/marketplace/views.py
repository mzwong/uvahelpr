from django.shortcuts import render
import urllib.request
import urllib.parse
import json


# Create your views here.
def index(request):
	return render(request, 'marketplace/index.html')

def job_entry(request, id):
	# make a GET request and parse the returned JSON                                                                                                                                                           # note, no timeouts, error handling or all the other things needed to do this for real
	#req = urllib.request.Request('http://www.mocky.io/v2/57f001943d0000dc1e0dd7ca')
	req = urllib.request.Request('http://exp-api:8000/jobs/' + id + '/')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp_dict = json.loads(resp_json)
	context = {"job": resp_dict}
	return render(request, 'marketplace/job_detail.html', context=context)

def allJobs(request):
	#Experience service call to get all jobs
	req = urllib.request.Request('http://exp-api:8000/jobs/')

	#mock response data for testing:
	#req = urllib.request.Request('http://www.mocky.io/v2/57efed1a3d0000371e0dd7c4')

	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	context = {'job_list' : resp}
	return render(request, 'marketplace/jobslist.html', context)



