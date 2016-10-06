from django.test import TestCase, RequestFactory
import json
from .views import UserRU, JobRU, MessageRU, get_all_jobs
from django.contrib.auth.models import User, AnonymousUser
from .models import Profile, Job, Message
from .forms import JobForm, MessageForm

class GetUsers(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.sample_user = User(username="faker", password="faker")
        self.sample_user.save()
        self.prof = Profile(phone_number="7324438712", skills="martial arts")
        self.prof.user = self.sample_user
        self.prof.save()

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
         for user in User.objects.all():
             user.delete()

class GetJobs(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.sample_user = User(username="faker", password="faker")
        self.sample_user.save()
        self.prof = Profile(phone_number="7324438712", skills="martial arts")
        self.prof.user = self.sample_user
        self.prof.save()
        job_args = {'skills_required': 'awesomeness',
         'requester_id': self.sample_user.id,
         'servicer_id': self.sample_user.id,
         'compensation': 10000,
         'event_time': '2009-08-09 11:00:00',
         'location': 'Charlottesville',
         'time_required': 30.00}
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

    def tearDown(self):
         for user in User.objects.all():
             user.delete()
         for job in Job.objects.all():
             job.delete()

class GetMessages(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.sample_user = User(username="faker", password="faker")
        self.sample_user.save()
        self.prof = Profile(phone_number="7324438712", skills="martial arts")
        self.prof.user = self.sample_user
        self.prof.save()
        message_args = {'skills_required': 'awesomeness',
         'recipient_id': self.sample_user.id,
         'sender_id': self.sample_user.id,
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
         for user in User.objects.all():
             user.delete()
         for message in Message.objects.all():
             message.delete()