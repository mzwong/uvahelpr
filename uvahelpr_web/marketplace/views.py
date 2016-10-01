from django.shortcuts import render
import urllib.request
import urllib.parse
import json


# Create your views here.
def index(request):
	return render(request, 'marketplace/index.html')

def allJobs(request):
	#Experience service call to get all jobs
	#req = urllib.request.Request('http://' + request.META['SERVER_NAME']+':8001/api/v1/users/3')

	#mock response data for testing:
	req = urllib.request.Request('http://www.mocky.io/v2/57efed1a3d0000371e0dd7c4')
	'''
	job1 = {"servicer_id": 4, "id": 1, "title": "Professor Needed", "description": "Our professor bailed and left the university and now no one will teach our class someone plz help", "compensation": "100.00", "requester_id": 2, "time_required": "2.00", "skills_required": "some", "location": "rice", "event_time": "2008-04-10T15:47:58Z"}
	job2 = {"servicer_id": 1, "id": 2, "title": "Tutoring", "description": "I'm a lowly padawan and I desperately need help with CS someone plz help me :(", "compensation": "1.50", "requester_id": 1, "time_required": "5.90", "skills_required": "something", "location": "ricehall", "event_time": "2009-06-11T21:02:09Z"}
	resp = {'result' : [job1, job2]}
	'''
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	context = {'job_list' : resp["result"]}
	return render(request, 'marketplace/jobslist.html', context)