from django.test import TestCase, Client
from accounts.models import User
from charities.models import Benefactor, Charity

class TestAll(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            "username": "AmitisH",
            "password": "123Aa123",
            "phone": "09381234567",
            "address": "Iran Tehran",
            "gender": "F",
            "age": "22",
            "description": "IDK",
            "first_name": "Seyed Amitis",
            "last_name": "Hashemi",
            "email": "amitisshashemii@gmail.com"
        }
        self.client.post('/accounts/register/', data=self.user_data, format='json')
        self.account1 = User.objects.get(username="AmitisH")

    def login_account(self):
        login_response = self.client.post('/accounts/login/', data={
            "username": self.user_data['username'],
            "password": self.user_data['password']
        }, format='json')
        self.assertEqual(login_response.status_code, 200)
        token = login_response.data['token']
        return {'HTTP_AUTHORIZATION': f'Token {token}'}

    def test_sample_benefactor_registration(self):
        header = self.login_account()
        response = self.client.post('/benefactors/', data={
            "experience": "2",
            "free_time_per_week": "5"
        }, format='json', **header)
        self.assertEqual(response.status_code, 201)
        benefactor = Benefactor.objects.first()
        self.assertIsNotNone(benefactor)
        self.assertEqual(benefactor.user, self.account1)
        self.assertEqual(benefactor.experience, 2)

    def test_sample_charity_registration(self):
        header = self.login_account()
        response = self.client.post('/charities/', data={
            "name": "Aseman",
            "reg_number": "9567549080"
        }, format='json', **header)
        self.assertEqual(response.status_code, 201)
        charity = Charity.objects.first()
        self.assertIsNotNone(charity)
        self.assertEqual(charity.name, "Aseman")
        self.assertEqual(charity.reg_number, "9567549080")
