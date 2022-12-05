from django.contrib.auth import get_user_model
from django.test import TestCase

from vinttem_api.transactions.models import Transaction


class TransactionModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='user_1',
                                                         password='pass123',
                                                         email='user_1@email.com')

        # self.user.save()
        # user = authenticate(username='user_1', password='pass123')
        self.obj = Transaction(
            type=Transaction.TransactionType.INCOME,
            description='descrição teste',
            value='12.34',
            owner=self.user,
        )
        self.obj.save()

    def tearDown(self):
        self.user.delete()

    def test_create(self):
        self.assertTrue(Transaction.objects.exists())
