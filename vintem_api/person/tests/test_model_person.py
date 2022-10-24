from django.test import TestCase

from vintem_api.person.models import Person


class PersonModelTest(TestCase):
    def setUp(self):
        self.obj = Person(
            name='Matheus Lopes',
            email='e@mail.com',
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Person.objects.exists())

    def test_email(self):
        self.assertEqual('e@mail.com', self.obj.email)
