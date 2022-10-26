from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from vintem_api.transactions.models import Transaction, TransactionSerializer


@api_view(['GET', 'POST'])
def transactions_list(request):
    if request.method == 'GET':
        transactions = Transaction.objects.all()
        t = TransactionSerializer(transactions, many=True)
        return Response(t.data)

    elif request.method == 'POST':
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
