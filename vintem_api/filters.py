from django_filters import FilterSet, DateTimeFilter, NumberFilter, AllValuesFilter, ChoiceFilter, DateFilter
from rest_framework import filters

from vintem_api.transactions.models import Transaction


class LoggedUserFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner=request.user)


class TransactionFilter(FilterSet):
    from_created_at = DateFilter(field_name='created_at', lookup_expr='gte')
    to_created_at = DateFilter(field_name='created_at', lookup_expr='lte')
    value = NumberFilter(field_name='value', lookup_expr='')
    description = AllValuesFilter(field_name='description')
    type = ChoiceFilter(field_name='type', choices=Transaction.TransactionType.choices)

    class Meta:
        model = Transaction
        fields = ['type', 'value', 'description', 'created_at']


class TransactionClosingFilter(FilterSet):
    from_created_at = DateFilter(field_name='created_at', lookup_expr='gte')
    to_created_at = DateFilter(field_name='created_at', lookup_expr='lte')
    expenses_sum = NumberFilter(field_name='expenses_sum', lookup_expr='')

    class Meta:
        model = Transaction
        fields = ['expenses_sum', 'created_at']
