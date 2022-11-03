from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from vintem_api.transactions.models import Transaction


class TransactionAPITest(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser('admin', 'admin@email.com', 'admin_password')

        self.client = APIClient()
        self.client.login(username='admin', password='admin_password')

    def test_get(self):
        """
        Ensure we can get a transaction object.
        """

        url = reverse('transactions:transaction-list')
        data = {
            "description": "test description",
            "value": 13,
            "type": Transaction.TransactionType.EXPENSE
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.get().description, 'test description')
