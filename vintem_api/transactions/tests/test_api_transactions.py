import pdb
from datetime import datetime, timedelta
from unittest import skip

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from vintem_api.transactions.models import Transaction

TRANSACTION_CREATE_AND_LIST_URL = reverse('transactions:transaction-list')
TRANSACTION_CLOSING_URL = reverse('transactions:transaction-closing')


def create_transaction(self, description='test description', value=1,
                       transaction_type=Transaction.TransactionType.EXPENSE):
    data = {
        "description": description,
        "value": value,
        "type": transaction_type
    }
    return self.client.post(TRANSACTION_CREATE_AND_LIST_URL, data)


class TransactionAPITest(APITestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user('user_1', 'user_1@email.com', 'user_1_password')
        self.user_2 = User.objects.create_user('user_2', 'user_2@email.com', 'user_2_password')
        self.client = APIClient()

    def tearDown(self):
        self.client.logout()

    def test_get(self):
        """
        Ensure we can get a transaction object.
        """
        self.client.login(username='user_1', password='user_1_password')
        transaction_1 = create_transaction(self, 'test description 1', 1, Transaction.TransactionType.EXPENSE) \
            .data

        url = reverse('transactions:transaction-detail', args=[transaction_1.get('id')])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.get().description, 'test description 1')

    def test_list(self):
        """
        Ensure we can list all logged user transactions
        """
        self.client.login(username='user_2', password='user_2_password')
        create_transaction(self, 'test description 2', 2, Transaction.TransactionType.EXPENSE)
        self.client.logout()

        self.client.login(username='user_1', password='user_1_password')
        create_transaction(self, 'test description 3', 3, Transaction.TransactionType.EXPENSE)

        response = self.client.get(TRANSACTION_CREATE_AND_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 1)

    def test_transactions_closing(self):
        """
        Ensure we can Sum all user expense transactions
        """
        self.client.login(username='user_1', password='user_1_password')
        create_transaction(self, 'test description 4', 4, Transaction.TransactionType.EXPENSE)
        create_transaction(self, 'test description 5', 5, Transaction.TransactionType.EXPENSE)

        data = {
            "start_date": datetime.today() - timedelta(days=1),
            "end_date": datetime.today() + timedelta(days=1)
        }
        response = self.client.get(TRANSACTION_CLOSING_URL, data)
        self.client.logout()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('expenses_total'), 9)
        self.assertEqual(response.data.get('owner_id'), self.user_1.id)

        self.client.login(username='user_2', password='user_2_password')
        create_transaction(self, 'test description 6', 6, Transaction.TransactionType.EXPENSE)

        response = self.client.get(TRANSACTION_CLOSING_URL, data)
        self.client.logout()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('expenses_total'), 6)
        self.assertEqual(response.data.get('owner_id'), self.user_2.id)
