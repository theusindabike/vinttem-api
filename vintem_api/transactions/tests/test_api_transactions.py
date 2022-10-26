from django.urls import reverse
from django.shortcuts import resolve_url as r
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from vintem_api.transactions.models import Transaction


class TransactionAPITest(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_get(self):
        """
        Ensure we can create a new transaction object.
        """
        #url = r('transactions')
        #data = {'type': Transaction.TransactionType.INCOME.label,
         #       'description': 'description test API',
          #      'value': '12.34'
           #     }
        response = self.client.get('http://127.0.0.1:8000/transactions/')
        #response = self.client.get(r('api:transactions.list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Transaction.objects.count(), 0)
        #self.assertEqual(Transaction.objects.get().name, 'DabApps')
