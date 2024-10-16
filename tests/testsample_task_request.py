from django.test import TestCase, Client
from rest_framework import status
from accounts.models import User
from charities.models import Charity, Benefactor, Task


class TaskTests(TestCase):
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

        # Register and log in the user
        self.client.post('/accounts/register/', data=self.user_data, format='json')
        self.user = User.objects.get(username=self.user_data['username'])
        self.header = self.login_account()

        # Create a charity
        self.client.post('/charities/', data={
            "name": "Aseman",
            "reg_number": "9567549080"
        }, format='json', **self.header)
        self.charity = Charity.objects.get(name="Aseman")

        # Create a benefactor
        self.client.post('/benefactors/', data={
            "experience": "2",
            "free_time_per_week": "4"
        }, format='json', **self.header)
        self.benefactor = Benefactor.objects.get(user=self.user)

        # Create tasks
        self.task1 = Task.objects.create(
            title='Sample Task 1',
            state='P',  # Pending
            charity=self.charity,
            description="Test Description"
        )
        self.task2 = Task.objects.create(
            title='Sample Task 2',
            state='W',  # Waiting
            charity=self.charity,
            description="Test Description",
            assigned_benefactor=self.benefactor
        )

    def login_account(self):
        login_response = self.client.post('/accounts/login/', data={
            "username": self.user_data['username'],
            "password": self.user_data['password']
        }, format='json')
        self.assertEqual(status.HTTP_200_OK, login_response.status_code)
        token = login_response.data['token']
        return {'HTTP_AUTHORIZATION': f'Token {token}'}

    def test_task_request_success(self):
        response = self.client.get(f'/tasks/{self.task2.id}/request/', data={}, format='json', **self.header)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.task2.refresh_from_db()
        self.assertEqual('W', self.task2.state)
        self.assertEqual(self.benefactor, self.task2.assigned_benefactor)
        self.assertEqual({'detail': 'Request sent.'}, response.data)

    def test_task_not_pending(self):
        response = self.client.get(f'/tasks/{self.task1.id}/request/', data={}, format='json', **self.header)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual({'detail': 'This task is not pending.'}, response.data)