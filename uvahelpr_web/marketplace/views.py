from django.shortcuts import render
import urllib.request
import urllib.parse
import json

# Create your views here.
def index(request):
	return render(request, 'marketplace/index.html')

def job_entry(request, id):
	# make a GET request and parse the returned JSON                                                                                                                                                           # note, no timeouts, error handling or all the other things needed to do this for real
	req = urllib.request.Request('http://www.mocky.io/v2/57f001943d0000dc1e0dd7ca')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp_dict = json.loads(resp_json)
	context = {"job": resp_dict["result"]}
	return render(request, 'marketplace/job_detail.html', context=context)