from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.utils import setup_test_environment
import urllib.request
import urllib.parse
import json
from urllib.parse import urlencode
from .views import login, create_job, search_listing
from django.test import TestCase, RequestFactory
from time import sleep
import subprocess
############################################
def requestHelperPost(url, postdata):
    post_encoded = urllib.parse.urlencode(postdata).encode('utf-8')
    req = urllib.request.Request('http://models-api:8000/api/v1/' + url, data=post_encoded, method='POST')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    return json.loads(resp_json)
############################################

class TestSearch(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        login_data = {'email': 'mzw7af@virginia.edu', 'password': 'pass123'}
        request = self.factory.post('/login/', data=login_data)
        resp = json.loads(login(request).content.decode('utf-8'))
        self.auth = resp['result']['authenticator']['authenticator']
        create_job_1 = {'skills_required': 'something',
                        'requester_id': 1,
                        'servicer_id': 1,
                        'compensation': 1.5,
                        'event_time': '2009-06-11 17:02:09',
                        'location': 'ricehall',
                        'time_required': 5.9,
                        'auth': self.auth,
                        'description': 'hello',
                        'title': 'isahw'
                        }
        create_job_2 = {'skills_required': 'stuff',
                        'requester_id': 1,
                        'servicer_id': 1,
                        'compensation': 14,
                        'event_time': '2049-02-11 10:25:09',
                        'location': 'uva',
                        'time_required': 5.9,
                        'auth': self.auth,
                        'description': 'world',
                        'title': 'isahw'
                        }
        create_job_3 = {'skills_required': 'uniqskillz',
                        'requester_id': 1,
                        'servicer_id': 1,
                        'compensation': 7,
                        'event_time': '2016-12-11 10:10:09',
                        'location': 'newplace',
                        'time_required': 100,
                        'auth': self.auth,
                        'description': 'desc',
                        'title': 'uniquetitle'
                        }
        request_1 = self.factory.post('/create_job/', data=create_job_1)
        resp_1 = json.loads(create_job(request_1).content.decode('utf-8'))
        self.job1_id = resp_1['result']['id']

        request_2 = self.factory.post('/create_job/', data=create_job_2)
        resp_2 = json.loads(create_job(request_2).content.decode('utf-8'))
        self.job2_id = resp_2['result']['id']

        request_3 = self.factory.post('/create_job/', data=create_job_3)
        resp_3 = json.loads(create_job(request_3).content.decode('utf-8'))
        self.job3_id = resp_3['result']['id']
        sleep(15)

    def testSearchUnique(self):
        search_data = {'query': 'uniquetitle'}
        request = self.factory.post('/search/', data=search_data)
        resp = json.loads(search_listing(request).content.decode('utf-8'))
        jobs = resp['result']
        self.assertEqual(len(jobs), 1)
        uniquejob = resp['result'][0]
        self.assertEqual(uniquejob['id'], self.job3_id)

    def testSearchDuplicate(self):
        search_data = {'query': 'isahw'}
        request = self.factory.post('/search/', data=search_data)
        resp = json.loads(search_listing(request).content.decode('utf-8'))
        jobs = resp['result']
        self.assertEqual(len(jobs), 2)
        dupsjob1 = resp['result'][0]
        dupsjob2 = resp['result'][1]
        expectedjobs = [self.job1_id, self.job2_id]
        self.assertTrue(dupsjob1['id'] != dupsjob2['id'])
        self.assertTrue(dupsjob1['id'] in expectedjobs)
        self.assertTrue(dupsjob2['id'] in expectedjobs)

    def testSearchNothing(self):
        search_data = {'query': 'nonexistent'}
        request = self.factory.post('/search/', data=search_data)
        resp = json.loads(search_listing(request).content.decode('utf-8'))
        jobs = resp['result']
        self.assertEqual(len(jobs), 0)

    def tearDown(self):
        removeES = "curl -XDELETE es:9200/_all"
        subprocess.call(removeES, shell=True)
        sleep(15)
        requestHelperPost('jobs/delete/', {'id': self.job1_id})
        requestHelperPost('jobs/delete/', {'id': self.job2_id})
        requestHelperPost('jobs/delete/', {'id': self.job3_id})


