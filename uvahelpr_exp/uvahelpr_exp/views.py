from django.http import HttpResponse
import urllib.request
import urllib.parse
import json

def get_all_jobs(request):
    req = urllib.request.Request('http://' + request.META['SERVER_NAME'] + ':8001/api/v1/jobs/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp_dict = json.loads(resp_json)
    filter = []
    for job in resp_dict['result']:
        newjob = {'id': job['id'], 'title': job['title'], 'description': job['description']}
        filter.append(newjob)
    result = json.dumps(filter)
    return HttpResponse(result)

def job_summary(request, id):
    req = urllib.request.Request('http://' + request.META['SERVER_NAME'] + ':8001/api/v1/jobs/' + id + '/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp_dict = json.loads(resp_json)
    job = resp_dict['result']
    newjob = {'id': job['id'], 'title': job['title'], 'description': job['description'], 'time_required': job['time_required'],
              'event_time': job['event_time'], 'skills_required': job['skills_required'], 'compensation': job['compensation'], 'location':job['location']}
    result = json.dumps(newjob)
    return HttpResponse(result)