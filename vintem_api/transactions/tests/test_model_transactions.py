from django.test import TestCase

from vintem_api.transactions.models import Transaction


class TransactionModelTest(TestCase):    
    def setUp(self):
        self.obj = Transaction(
            type=Transaction.TransactionType.INCOME,
            description='descrição teste',
            value='12.34'
        )
        self.obj.save()

    
    # def test_create(self):
    #     self.assertTrue(Transaction.objects.exists())


