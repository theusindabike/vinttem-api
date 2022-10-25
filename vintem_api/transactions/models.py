from django.db import models
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


from vintem_api.person.models import Person


class Transaction(models.Model):

    class TransactionType(models.TextChoices):
        INCOME = 'I',
        EXPENSE = 'E',

    #person = models.ForeignKey(Person, on_delete=models.CASCADE)
    kind = models.CharField('tipo', max_length=1, choices=TransactionType.choices)
    description = models.CharField('descrição', max_length=255)
    value = models.DecimalField('valor', max_digits=16, decimal_places=2)
    created_at = models.DateTimeField('criado em', auto_now_add=True)


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transaction
        fields = ('description', 'value', 'kind', 'created_at')