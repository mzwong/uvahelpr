from django.http import HttpResponse
import urllib.request
import urllib.parse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

#this is probably a huge security issue.... needs to be fixed! #TODO
@csrf_exempt
def login(request):
    post_data = request.POST.dict()
    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
    req = urllib.request.Request('http://models-api:8000/api/v1/login/', data=post_encoded, method='POST')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return JsonResponse(resp)

def get_all_jobs(request):
    req = urllib.request.Request('http://models-api:8000/api/v1/jobs/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp_dict = json.loads(resp_json)
    jobarray = []
    for job in resp_dict['result']:
        newjob = {'id': job['id'], 'title': job['title'], 'description': job['description']}
        jobarray.append(newjob)
    result = {'result': jobarray, 'ok': True}
    return JsonResponse(result)

def job_summary(request, id):
    req = urllib.request.Request('http://models-api:8000/api/v1/jobs/' + id + '/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp_dict = json.loads(resp_json)
    job = resp_dict['result']
    user_id = str(job['requester'])

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

@csrf_exempt
def create_job(request):
    post_data = request.Post.dict()
    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
    req = urllib.request.Request('http://models-api:8000/api/v1/create_job/', data=post_encoded, method='POST')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return JsonResponse(resp)
