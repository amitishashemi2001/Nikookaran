from django.test import TestCase, Client
from accounts.models import User
from charities.models import Charity, Benefactor, Task
from rest_framework import status

class TestAll(TestCase):
    def login_account(self):
        login_response = self.client.post('/accounts/login/', data={
            "username": self.user_data['username'],
            "password": self.user_data['password']
        }, format='json')
        self.assertEqual(status.HTTP_200_OK, login_response.status_code)
        token = login_response.data['token']
        return {'HTTP_AUTHORIZATION': 'Token ' + token}

    def setUp(self):
        self.client = Client()
        self.user_data = {
            "username": "AmitisH",
            "password": "123Aa123",
            "phone": "09381234567",
            "address": "Iran Tehran",
            "gender": "F",
            "age": 22,
            "description": "IDK",
            "first_name": "Seyed Amitis",
            "last_name": "Hashemi",
            "email": "amitisshashemii@gmail.com"
        }
        self.client.post('/accounts/register/', data=self.user_data, format='json')
        self.account1 = User.objects.get(username=self.user_data["username"])
        self.header = self.login_account()

        self.client.post('/charities/', data={
            "name": "Aseman",
            "reg_number": "9567549080"
        }, format='json', **self.header)
        self.sample_charity = Charity.objects.get(name="Aseman")

        self.client.post('/benefactors/', data={
            "experience": "2",
            "free_time_per_week": "4"
        }, format='json', **self.header)
        self.sample_benefactor = Benefactor.objects.get(user=self.account1)

        self.sample_task1 = Task.objects.create(
            title='Sample Task 1',
            state='P',
            charity=self.sample_charity,
            description="Test Description",
        )
        self.sample_task2 = Task.objects.create(
            title='Sample Task 2',
            state='A',
            charity=self.sample_charity,
            description="Test Description",
        )

    def test_sample_task_not_assigned(self):
        sample_test1 = self.client.post('/tasks/1/done/', data={}, format='json', **self.header)
        self.assertEqual(status.HTTP_404_NOT_FOUND, sample_test1.status_code)
        self.assertEqual({'detail': 'Task is not assigned yet.'}, sample_test1.data)

    def test_sample_task_done(self):
        sample_test2 = self.client.post('/tasks/2/done/', data={}, format='json', **self.header)
        self.assertEqual(status.HTTP_200_OK, sample_test2.status_code)
        self.assertEqual({'detail': 'Task has been done successfully.'}, sample_test2.data)
        self.sample_task2.refresh_from_db()
        self.assertEqual('D', self.sample_task2.state)