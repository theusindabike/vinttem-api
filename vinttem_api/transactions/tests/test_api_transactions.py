from datetime import datetime

from django.contrib.auth.models import User
from django.urls import reverse
from pytz import timezone as tz
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from vinttem_api.transactions.models import Transaction

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
    fixtures = ['transactions.json', 'users.json']

    def setUp(self):
        self.user_1 = User.objects.get(pk=1)
        self.user_2 = User.objects.get(pk=2)
        self.client = APIClient()

    def tearDown(self):
        self.client.force_authenticate(user=None)

    def test_get(self):
        """
        Ensure we can get a transaction object.
        """
        t = Transaction.objects.get(id=1)

        self.client.force_authenticate(user=self.user_1)

        url = reverse('transactions:transaction-detail', args=[t.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), 1)
        self.assertEqual(response.data.get('description'), 'description test 1')

    def test_list(self):
        """
        Ensure we can list all logged user transactions
        """
        self.client.force_authenticate(user=self.user_1)

        response = self.client.get(TRANSACTION_CREATE_AND_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 6)

    def test_transactions_closing(self):
        """
        Ensure we can Sum all user expense and income transactions
        """
        data = {
            "from_created_at": datetime(2022, 4, 1, tzinfo=tz('America/Sao_Paulo')).strftime("%Y-%m-%d"),
            "to_created_at": datetime(2022, 4, 30, tzinfo=tz('America/Sao_Paulo')).strftime("%Y-%m-%d")
        }

        self.client.force_authenticate(user=self.user_1)
        user_1_response = self.client.get(TRANSACTION_CLOSING_URL, data)
        self.client.force_authenticate(user=None)

        self.client.force_authenticate(user=self.user_2)
        user_2_response = self.client.get(TRANSACTION_CLOSING_URL, data)
        self.client.force_authenticate(user=None)

        self.assertEqual(user_1_response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_1_response.data.get('expenses_total'), 10)
        self.assertEqual(user_1_response.data.get('owner_id'), self.user_1.id)

        self.assertEqual(user_2_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_closing_date_filter(self):
        """
        Ensure that start and end date filters work
        """
        self.client.login(username='user_1', password='user_1_password')
