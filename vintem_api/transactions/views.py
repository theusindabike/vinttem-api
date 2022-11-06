from rest_framework import permissions, generics

from vintem_api.filters import LoggedUserFilter
from vintem_api.transactions.models import Transaction, TransactionSerializer
from vintem_api.transactions.permissions import IsOwnerOrReadOnly


class TransactionList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all().order_by('id')
    filter_backends = [LoggedUserFilter]
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class TransactionClosing(generics.ListAPIView):
    pass
