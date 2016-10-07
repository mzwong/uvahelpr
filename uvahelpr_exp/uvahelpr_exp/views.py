from django.http import HttpResponse
import urllib.request
import urllib.parse
import json
from django.http import JsonResponse

def get_all_jobs(request):
    req = urllib.request.Request('http://models-api:8000/api/v1/jobs/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp_dict = json.loads(resp_json)
    fields = []
    for job in resp_dict['result']:
        newjob = {'id': job['id'], 'title': job['title'], 'description': job['description']}
        fields.append(newjob)

    result = {'result': fields, 'ok': True}
    return JsonResponse(result)

def job_summary(request, id):
    req = urllib.request.Request('http://models-api:8000/api/v1/jobs/' + id + '/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp_dict = json.loads(resp_json)
    job = resp_dict['result']
    user_id = str(job['requester_id'])

    req_user = urllib.request.Request('http://models-api:8000/api/v1/users/' + user_id + '/')
    user_json = urllib.request.urlopen(req_user).read().decode('utf-8')
    user_dict = json.loads(user_json)
    user_info = user_dict['result']
    firstname = user_info["first_name"]
    lastname = user_info['last_name']
    name = firstname + ' ' + lastname

    result = {x: job[x] for x in ['id', 'title', 'description', 'time_required', 'event_time', 'skills_required', 'compensation', 'location']}
    result['requester'] = name
    jsonresult = {'result': result, 'ok': True}
    return JsonResponse(jsonresult)

