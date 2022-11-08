from django.db import models
from django.db.models import Sum
from rest_framework import serializers


class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        INCOME = 'I',
        EXPENSE = 'E',

    owner = models.ForeignKey('auth.User', related_name='transactions', on_delete=models.CASCADE)
    type = models.CharField('tipo', max_length=1, choices=TransactionType.choices)
    description = models.CharField('descrição', max_length=255, null=True, blank=True)
    value = models.DecimalField('valor', max_digits=16, decimal_places=2)
    created_at = models.DateTimeField('criado em', auto_now_add=True)


class TransactionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Transaction
        fields = ['id', 'description', 'value', 'type', 'owner', 'created_at']


class TransactionClosingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    expenses_total = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        #fields = ['expenses_total', 'income_total', 'owner', 'created_at']
        fields = ['expenses_total', 'owner', 'created_at']

    def get_expenses_total(self, obj):
        #t = Transaction.objects.all().filter(owner=self.context['request'].user)
        return obj.filter(type='E').aggregate(expenses_total=Sum('value'))

