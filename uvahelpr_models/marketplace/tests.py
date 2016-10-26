from django.test import TestCase, RequestFactory
import json
from .views import *
from django.contrib.auth.models import AnonymousUser
from .models import HelprUser, Job, Message
from .forms import JobForm, MessageForm, HelprUserForm
from urllib.parse import urlencode

class GetUsers(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        user_args = {
            'username':"faker",
            'password':"faker",
            'email':"gg@virginia.edu" ,
            'first_name':"sensei",
            'last_name':"senpai",
            'phone_number':"7324438712",
            'skills':"martial arts"
        }
        self.sample_user_form = HelprUserForm(user_args)
        self.sample_user = self.sample_user_form.save()

    def test_getting_user_fails_bad_id(self):
        request = self.factory.get('/api/v1/users/')
        request.user = AnonymousUser()
        response = UserRU.as_view()(request, 1*10**6)
        self.assertEqual(response.status_code, 200)
        resp_dict = json.loads(response.content.decode())
        self.assertTrue(resp_dict["ok"]==False)

    def test_getting_user_succeeds(self):
        request = self.factory.get('/api/v1/users/')
        request.user = AnonymousUser()
        response = UserRU.as_view()(request, self.sample_user.id)
        self.assertEqual(response.status_code, 200)
        resp_dict = json.loads(response.content.decode())
        self.assertTrue(resp_dict["ok"]==True)
        self.assertTrue(len(resp_dict["result"])!=0)

    def tearDown(self):
         for user in HelprUser.objects.all():
             user.delete()

class TestJobs(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        user_args = {
            'username':"faker",
            'password':"faker",
            'email':"gg@virginia.edu" ,
            'first_name':"sensei",
            'last_name':"senpai",
            'phone_number':"7324438712",
            'skills':"martial arts"
        }
        self.sample_user_form = HelprUserForm(user_args)
        self.sample_user = self.sample_user_form.save()
        job_args = {'skills_required': 'awesomeness',
         'requester': self.sample_user.id,
         'servicer': self.sample_user.id,
         'compensation': 10000,
         'event_time': '2009-08-09 11:00:00',
         'location': 'Charlottesville',
         'time_required': 30.00,
         'title': 'Help needed',
         'description': 'I really really really need help.'
        }
        sample_job = JobForm(job_args)
        self.sample_job = sample_job.save()

    def test_getting_all_jobs(self):
        request = self.factory.get('/api/v1/jobs/')
        request.user = AnonymousUser()
        response = get_all_jobs(request)
        self.assertEqual(response.status_code, 200)
        resp_dict = json.loads(response.content.decode())
        self.assertTrue(resp_dict["ok"]==True)
        self.assertTrue(len(resp_dict["result"])!=0)

    def test_getting_job_fails_bad_id(self):
        request = self.factory.get('/api/v1/jobs/')
        request.user = AnonymousUser()
        response = JobRU.as_view()(request, 1*10**6)
        self.assertEqual(response.status_code, 200)
        resp_dict = json.loads(response.content.decode())
        self.assertTrue(resp_dict["ok"]==False)

    def test_getting_job_succeeds(self):
        request = self.factory.get('/api/v1/jobs/')
        request.user = AnonymousUser()
        response = JobRU.as_view()(request, self.sample_job.id)
        self.assertEqual(response.status_code, 200)
        resp_dict = json.loads(response.content.decode())
        self.assertTrue(resp_dict["ok"]==True)
        self.assertTrue(len(resp_dict["result"])!=0)

    def test_create_job_missing_fields(self):
        job_data = {
            'skills_required': 'being smart',
            'requester': self.sample_user.id,
            'compensation': 100,
            'event_time': '2009-08-09 11:00:00',
            'location': 'Charlottesville',
            'time_required': 70.00,
            'title': 'Tutor Needed',
            'description': 'Im so lost.'
        }
        request = self.factory.post(path='/api/v1/jobs/create/', data=job_data)
        response = create_job(request)
        result_dict = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(result_dict["ok"])
        self.assertTrue(len(Job.objects.all()) == 2)
        self.assertEqual(result_dict["result"]['id'], 2)

    def test_create_job_success(self):
        job_data = {
            'skills_required': 'being smart',
            'requester': self.sample_user.id,
            'compensation': 100,
            'time_required': 70.00,
            'title': 'Tutor Needed',
            'description': 'Im so lost.'
        }
        request = self.factory.post(path='/api/v1/jobs/create/', data=job_data)
        response = create_job(request)
        result_dict = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertFalse(result_dict["ok"])
        self.assertTrue(len(Job.objects.all()) == 1)
        self.assertEqual(result_dict["result"], "Invalid form data.")

    def test_delete_job_invalid(self):
        job_data = {
            'id': 999
        }
        request = self.factory.post(path='/api/v1/jobs/delete/', data=job_data)
        response = delete_job(request)
        result_dict = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertFalse(result_dict["ok"])
        self.assertTrue(len(Job.objects.all()) == 1)
        self.assertEqual(result_dict["result"], "Job does not exist.")

    def test_delete_job_success(self):
        job_data = {
            'id': self.sample_job.id
        }
        request = self.factory.post(path='/api/v1/jobs/delete/', data=job_data)
        response = delete_job(request)
        result_dict = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(result_dict["ok"])
        self.assertTrue(len(Job.objects.all()) == 0)
        self.assertEqual(result_dict["result"], "Job succesfully deleted.")

    def tearDown(self):
         for user in HelprUser.objects.all():
             user.delete()
         for job in Job.objects.all():
             job.delete()

class GetMessages(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        user_args = {
            'username':"faker",
            'password':"faker",
            'email':"gg@virginia.edu" ,
            'first_name':"sensei",
            'last_name':"senpai",
            'phone_number':"7324438712",
            'skills':"martial arts"
        }
        self.sample_user_form = HelprUserForm(user_args)
        self.sample_user = self.sample_user_form.save()
        message_args = {'skills_required': 'awesomeness',
         'recipient': self.sample_user.id,
         'sender': self.sample_user.id,
         'text_body': "Hello world!",
         'time_sent': '2009-08-09 11:00:00',
         }
        sample_message = MessageForm(message_args)
        self.sample_message = sample_message.save()

    def test_getting_message_details_fails(self):
        request = self.factory.get('/api/v1/messages/')
        request.user = AnonymousUser()
        response = MessageRU.as_view()(request, 1*10**6)
        result_dict = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(result_dict["ok"]==False)

    def test_getting_message_details_succeeds(self):
        request = self.factory.get('/api/v1/messages/')
        request.user = AnonymousUser()
        response = MessageRU.as_view()(request, self.sample_message.id)
        result_dict = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(result_dict["ok"]==True)
        self.assertTrue(len(result_dict["result"])!=0)

    def tearDown(self):
         for user in HelprUser.objects.all():
             user.delete()
         for message in Message.objects.all():
             message.delete()

class CreateUser(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        user_args = {
            'username':"faker",
            'password':"faker",
            'email':"gg@virginia.edu" ,
            'first_name':"sensei",
            'last_name':"senpai",
            'phone_number':"7324438712",
            'skills':"martial arts"
        }
        self.sample_user_form = HelprUserForm(user_args)
        self.sample_user = self.sample_user_form.save()

    def test_adding_user_incomplete_info_fails(self):
        user_data = {
            "username": "new_user",
            "password":"new_user",
            "email": "blahblah@virginia.edu",
        }
        request = self.factory.post(path='/api/v1/users/create/', data=user_data)
        response =  create_user(request)
        result_dict = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(result_dict["ok"]==False)
        self.assertTrue(len(HelprUser.objects.all())==1)
        self.assertTrue(result_dict["result"]=="Input did not contain all the required fields.")

    def test_adding_user_invalid_phone_number_fails(self):
        user_data = {
            'username':"new_user",
            'password':"new_user",
            'email':"blahblah@virginia.edu" ,
            'first_name':"sensei",
            'last_name':"senpai",
            'phone_number':"7324438712ABC",
            'skills':"martial arts"
        }
        request = self.factory.post(path='/api/v1/users/create/', data=user_data)
        response =  create_user(request)
        result_dict = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(result_dict["ok"]==False)
        self.assertTrue(len(HelprUser.objects.all())==1)
        self.assertTrue(result_dict["result"]=="Invalid form data.")
        self.assertTrue(len(HelprUser.objects.filter(username='new_user'))==0)


    def test_adding_user_duplicate_username_fails(self):
        user_data = {
            'username':"faker",
            'password':"new_user",
            'email':"blahblah@virginia.edu" ,
            'first_name':"sensei",
            'last_name':"senpai",
            'phone_number':"7324438712",
            'skills':"martial arts"
        }
        request = self.factory.post(path='/api/v1/users/create/', data=user_data)
        response =  create_user(request)
        result_dict = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(result_dict["ok"]==False)
        self.assertTrue(len(HelprUser.objects.all())==1)
        self.assertTrue(len(HelprUser.objects.filter(username='new_user'))==0)

    def test_adding_user_duplicate_email_fails(self):
        user_data = {
            'username':"new_user",
            'password':"new_user",
            'email':"gg@virginia.edu" ,
            'first_name':"sensei",
            'last_name':"senpai",
            'phone_number':"7324438712",
            'skills':"martial arts"
        }
        request = self.factory.post(path='/api/v1/users/create/', data=user_data)
        response =  create_user(request)
        result_dict = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(result_dict["ok"]==False)
        self.assertTrue(len(HelprUser.objects.all())==1)
        self.assertTrue(len(HelprUser.objects.filter(username='new_user'))==0)

    def test_adding_user_succeeds(self):
        user_data = {
            'username':"new_user",
            'password':"new_user",
            'email':"new_user@virginia.edu" ,
            'first_name':"sensei",
            'last_name':"senpai",
            'phone_number':"7324438712",
            'skills':"martial arts"
        }
        request = self.factory.post(path='/api/v1/users/create/', data=user_data)
        response =  create_user(request)
        result_dict = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(result_dict["ok"]==True)
        self.assertTrue(len(HelprUser.objects.all())==2)
        self.assertTrue(len(HelprUser.objects.filter(email="new_user@virginia.edu"))==1)

    def tearDown(self):
         for user in HelprUser.objects.all():
             user.delete()
