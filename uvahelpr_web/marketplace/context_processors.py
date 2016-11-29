import urllib.request
import urllib.parse
import json, os
from .forms import SearchForm

def loggedIn_processor(request):
    try:
        authkey = request.COOKIES["auth"]
    except KeyError:
        return {"loggedin" : False}
    post_data = {'auth' : authkey}
    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
    req = urllib.request.Request('http://exp-api:8000/auth-user/', data=post_encoded, method='POST')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    if resp['ok']:
        first_name = resp['result']
        return {'logged_in_user_name' : first_name, 'loggedin': True}
    else:
        return {'loggedin': False}

def searchbar_processor(request):
    header_search_bar = SearchForm()
    return {'search_form': header_search_bar}

def webservername_processor(request):
    return {'container': os.environ['EXP_API_NAME'][1:-10]}