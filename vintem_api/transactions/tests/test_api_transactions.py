import pdb
from datetime import datetime, timedelta
from unittest import skip

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from vintem_api.transactions.models import Transaction


class TransactionAPITest(APITestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user('user_1', 'user_1@email.com', 'user_1_password')
        self.user_2 = User.objects.create_user('user_2', 'user_2@email.com', 'user_2_password')
        self.client = APIClient()

        self.client.login(username='user_1', password='user_1_password')

        url = reverse('transactions:transaction-list')
        data = {
            "description": "test description 1",
            "value": 11,
            "type": Transaction.TransactionType.EXPENSE
        }
        self.client.post(url, data)
        self.client.logout()

    def tearDown(self):
        self.client.logout()

    def test_get(self):
        """
        Ensure we can get a transaction object.
        """
        url = reverse('transactions:transaction-detail', args=[self.user_1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.get().description, 'test description 1')

    def test_list(self):
        """
        Ensure we can list all logged user transactions
        """
        self.client.login(username='user_2', password='user_2_password')
        url = reverse('transactions:transaction-list')
        data = {
            "description": "test description 2",
            "value": 12,
            "type": Transaction.TransactionType.EXPENSE
        }
        self.client.post(url, data)
        self.client.logout()

        self.client.login(username='user_1', password='user_1_password')
        url = reverse('transactions:transaction-list')
        data = {
            "description": "test description 3",
            "value": 13,
            "type": Transaction.TransactionType.INCOME
        }
        self.client.post(url, data)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Transaction.objects.count(), 3)

    @skip("")
    def test_expenses_sum(self):
        """
        Ensure we can Sum all user expense transactions
        """
        self.client.login(username='user_1', password='user_1_password')
        url = reverse('transactions:transaction-list')
        data = {
            "description": "test description 2",
            "value": 1313.13,
            "type": Transaction.TransactionType.EXPENSE
        }
        self.client.post(url, data)

        url = reverse('transactions:transaction-closing')
        data = {
            "start_date": datetime.today() - timedelta(days=1),
            "end_date": datetime.today() + timedelta(days=1)
        }
        response = self.client.get(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(Transaction.objects.count(), 2)
