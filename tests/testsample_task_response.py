from django.test import TestCase, Client
from rest_framework import status
from accounts.models import User
from charities.models import Charity, Benefactor, Task


class TaskResponseTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Register and log in the user
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
        self.user = User.objects.get(username=self.user_data['username'])
        self.header = self.login_account()

        # Create charity
        self.client.post('/charities/', data={
            "name": "Aseman",
            "reg_number": "9567549080"
        }, format='json', **self.header)
        self.charity = Charity.objects.get(name="Aseman")

        # Create benefactor
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
            description="Test Description",
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

    def test_invalid_task_response(self):
        # Test for invalid response value
        response = self.client.post(f'/tasks/{self.task1.id}/response/', data={
            "response": "D",  # Invalid response
        }, format='json', **self.header)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual({'detail': 'Required field ("A" for accepted / "R" for rejected)'}, response.data)

    def test_accept_task(self):
        # Test for valid accept response
        response = self.client.post(f'/tasks/{self.task2.id}/response/', data={
            "response": "A",  # Accept the task
        }, format='json', **self.header)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual({'detail': 'Response sent.'}, response.data)
        self.task2.refresh_from_db()
        self.assertEqual('A', self.task2.state)  # Task state should be updated to 'Assigned'