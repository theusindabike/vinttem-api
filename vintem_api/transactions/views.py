from django.db.models import Sum, Min, Max
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, generics
from rest_framework.response import Response

from vintem_api.filters import LoggedUserFilter, TransactionClosingFilter, TransactionFilter
from vintem_api.transactions.models import Transaction, TransactionSerializer


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


class TransactionClosing(generics.RetrieveAPIView):
    queryset = Transaction.objects.all().order_by('id')
    filter_backends = [LoggedUserFilter, DjangoFilterBackend]
    filterset_class = TransactionClosingFilter
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        try:
            owner_id = queryset.first().owner_id

            expenses_total = queryset.filter(type='E').aggregate(expenses_total=Sum('value'))
            incomes_total = queryset.filter(type='I').aggregate(incomes_total=Sum('value'))

            min_date = queryset.aggregate(min_date=Min('created_at'))
            max_date = queryset.aggregate(max_date=Max('created_at'))

            data = expenses_total | incomes_total | min_date | max_date | {'owner_id': owner_id}
            return Response(data)
        except:
            raise Http404("No transactions found")
