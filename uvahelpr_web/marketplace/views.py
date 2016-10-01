from django.shortcuts import render
import urllib.request
import urllib.parse
import json
from django.http import HttpResponse

# Create your views here.
def index(request):
	return render(request, 'marketplace/index.html')

def allJobs(request):
	#Experience service call to get all jobs
	req = urllib.request.Request('http://' + request.META['SERVER_NAME']+':8002/jobs/')

	#mock response data for testing:
	#req = urllib.request.Request('http://www.mocky.io/v2/57efed1a3d0000371e0dd7c4')

	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	context = {'job_list' : resp["result"]}
	return render(request, 'marketplace/jobslist.html', context)