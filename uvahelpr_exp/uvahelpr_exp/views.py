from django.http import HttpResponse
import urllib.request
import urllib.parse
import json
import datetime
from django.utils import timezone
from django.http import JsonResponse
from kafka import KafkaProducer
from elasticsearch import Elasticsearch, ElasticsearchException

#Helper functions for making requests to the models layer
###########################################
def requestHelperPost(url, postdata):
    post_encoded = urllib.parse.urlencode(postdata).encode('utf-8')
    req = urllib.request.Request('http://models-api:8000/api/v1/' + url, data=post_encoded, method='POST')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    return json.loads(resp_json)

def requestHelperGet(url):
    req = urllib.request.Request('http://models-api:8000/api/v1/' + url)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    return json.loads(resp_json)
############################################

def login(request):
    post_data = request.POST.dict()
    user_info = requestHelperPost('check_password/', post_data)
    if user_info['ok']:
        post_data2 = {'user_id': user_info['result']['id']}
        resp = requestHelperPost('create_authenticator/', post_data2)
    else:
        resp = user_info
    return JsonResponse(resp)

def logout(request):
    post_data = request.POST.dict()
    resp = requestHelperPost('delete_authenticator/', post_data)
    return JsonResponse(resp)

def create_account(request):
    post_data = request.POST.dict()
    resp = requestHelperPost('users/create/', post_data)
    return JsonResponse(resp)

def getAuthUser(request):
    post_data = request.POST.dict()
    resp = requestHelperPost('auth_user/', post_data)
    authenticator_valid = True
    if resp['ok']:
        authenticator = resp['result']['auth']
        if authenticator['time_created'] < (timezone.now() - datetime.timedelta(days=1)).isoformat():
            authenticator_valid = False
    else:
        authenticator_valid = False
    if authenticator_valid:
        first_name = resp['result']['user']['first_name']
        result = {'result': first_name, 'ok': True}
    else:
        result = {'result': 'Invalid authenticator', 'ok': False}
    return JsonResponse(result)

def get_all_jobs(request):
    resp_dict = requestHelperGet('jobs/')
    jobarray = []
    for job in resp_dict['result']:
        newjob = {'id': job['id'], 'title': job['title'], 'description': job['description']}
        jobarray.append(newjob)
    result = {'result': jobarray, 'ok': True}
    return JsonResponse(result)

def job_summary(request, id):
    resp_dict = requestHelperGet('jobs/' + id + '/')
    job = resp_dict['result']
    user_id = str(job['requester'])

    user_dict = requestHelperGet('users/' + user_id + '/')
    user_info = user_dict['result']
    firstname = user_info["first_name"]
    lastname = user_info['last_name']
    name = firstname + ' ' + lastname

    result = {x: job[x] for x in ['id', 'title', 'description', 'time_required', 'event_time', 'skills_required', 'compensation', 'location']}
    result['requester'] = name
    jsonresult = {'result': result, 'ok': True}
    return JsonResponse(jsonresult)

def create_job(request):
    post_data = request.POST.dict()
    auth = post_data.get('auth')
    post_data.pop('auth')
    auth_dict = {'auth': auth}
    user = requestHelperPost('auth_user/', auth_dict)
    if user['ok']:
        post_data['requester'] = user['result']['user']['id']
        resp = requestHelperPost('create_job/', post_data)
        # if the user is valid send the new listing to the kafka queue as well as the model layer api
        if resp['ok']:
            job_resp =  requestHelperGet('jobs/' + str(resp['result']['id']) + '/')
            producer = KafkaProducer(bootstrap_servers='kafka:9092')
            producer.send('new-listings-topic', json.dumps(job_resp["result"]).encode('utf-8'))
    else:
        resp = {'result': 'Invalid authenticator', 'ok': False}
    return JsonResponse(resp)

def search_listing(request):
    post_data = request.POST.dict()
    query = post_data.get('query')
    resp = {}
    try:
        es = Elasticsearch(['es'])
        search_res = es.search(index='listing_index', body={'query': {'query_string': {'query': query}}, 'size': 100})
        resp['ok'] = True
        resp['result'] = []
        for hit in search_res['hits']['hits']:
            resp['result'].append(hit['_source'])
    except ElasticsearchException as e:
        resp['ok'] = False
        resp['result'] = e
    return JsonResponse(resp)