from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.utils import setup_test_environment
import urllib.request
import urllib.parse
import json

# class GetJobSummaryTestCase(TestCase):
#   def setUp(self):     #setUp method is called before each test in this class
#      setup_test_environment()
#
#   def test_success_response(self):
#      checkout_url = '{}{}'.format(self.live_server_url, reverse('checkout', kwargs={'pk': article.id}))
#      parsed_url = urlparse(self.live_server_url)
#      response = self.client.get(checkout_url, SERVER_NAME=parsed_url.hostname, SERVER_PORT=parsed_url.port)
#      url = reverse('get_job', kwargs={'id':1})
#      print("Calling {}".format(url))
#      response = self.client.get(url)   #assumes job with id 1 is stored in db
#      self.assertEquals(response.status_code, 200)
#
#   def tearDown(self):  #tearDown method is called after each test
#      pass              #nothing to tear down