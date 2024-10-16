from django.test import TestCase, Client
from accounts.models import User

class TestAll(TestCase):
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

    def test_sample_sign_up(self):
        account = User.objects.get(username=self.user_data['username'])
        self.assertEqual(account.username, self.user_data['username'])
        self.assertEqual(account.gender, self.user_data['gender'])
        self.assertEqual(account.age, self.user_data['age'])
        self.assertEqual(account.phone, self.user_data['phone'])
        self.assertEqual(account.address, self.user_data['address'])
        self.assertEqual(account.first_name, self.user_data['first_name'])
        self.assertEqual(account.last_name, self.user_data['last_name'])
        self.assertEqual(account.email, self.user_data['email'])
        self.assertEqual(account.description, self.user_data['description'])

    def test_sample_log_in(self):
        login_response = self.client.post('/accounts/login/', data={
            "username": self.user_data['username'],
            "password": self.user_data['password']
        }, format='json')

        self.assertEqual(login_response.status_code, 200)
        self.assertIn('token', login_response.data)
