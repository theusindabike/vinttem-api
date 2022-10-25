from rest_framework import viewsets
from rest_framework import permissions
from vintem_api.transactions.models import Transaction, TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    #permission_classes = [permissions.IsAuthenticated]
