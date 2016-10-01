from django.http import HttpResponse
import urllib.request
import urllib.parse

def get_all_jobs(request):
    req = urllib.request.Request('http://' + request.META['SERVER_NAME'] + ':8001/api/v1/jobs/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    return HttpResponse(resp_json)