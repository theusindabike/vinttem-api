import pdb

from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from vintem_api.filters import LoggedUserFilter, TransactionClosingFilter, TransactionFilter
from vintem_api.transactions.models import Transaction, TransactionSerializer, TransactionClosingSerializer


class TransactionList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all().order_by('id')
    serializer_class = TransactionSerializer
    filter_backends = [LoggedUserFilter, DjangoFilterBackend]
    filterset_class = TransactionFilter
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all().order_by('id')
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]


class TransactionClosing(generics.ListAPIView):
    queryset = Transaction.objects.all().order_by('id')
    filter_backends = [LoggedUserFilter, DjangoFilterBackend]
    filterset_class = TransactionClosingFilter
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        expenses_total = queryset.filter(type='E').aggregate(expenses_total=Sum('value'))
        incomes_total = queryset.filter(type='I').aggregate(incomes_total=Sum('value'))

        data = expenses_total | incomes_total
        return Response(data)
