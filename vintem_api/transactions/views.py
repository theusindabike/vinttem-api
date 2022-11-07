from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, generics

from vintem_api.filters import LoggedUserFilter, TransactionClosingFilter, TransactionFilter
from vintem_api.transactions.models import Transaction, TransactionSerializer, TransactionClosingSerializer


class TransactionList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all().order_by('id')
    serializer_class = TransactionSerializer
    filter_backends = [LoggedUserFilter, DjangoFilterBackend]
    filterset_class = TransactionFilter
    permission_classes = [permissions.IsAuthenticated]
    #filterset_fields = ('id', 'type', 'created_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all().order_by('id')
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]


class TransactionClosing(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionClosingSerializer
    filter_backends = [LoggedUserFilter, DjangoFilterBackend]
    filter_class = TransactionClosingFilter
    permission_classes = [permissions.IsAuthenticated]
    # filterset_fields = [
    #     'expenses_sum',
    # ]

# def get_queryset(self):
#     queryset = Transaction.objects.all().order_by('id')
#     start_date = self.request.query_params.get('start_date', None)
#     end_date = self.request.query_params.get('end_date', None)
#
#     if start_date is not None and end_date is not None:
#         queryset = queryset.filter(created_at__gte=start_date, created_at__lte=end_date)
#
#     return queryset
