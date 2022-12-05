from django.contrib import admin

from vinttem_api.transactions.models import Transaction


class TransactionModelAdmin(admin.ModelAdmin):
    list_display = ('type', 'description', 'value', 'created_at', 'owner')
    date_hierarchy = 'created_at'
    search_fields = ('type', 'description', 'value', 'created_at', 'owner')
    list_filter = ('created_at',)


admin.site.register(Transaction, TransactionModelAdmin)
