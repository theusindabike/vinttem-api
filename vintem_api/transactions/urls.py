from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'transactions'

urlpatterns = [
    path('', views.TransactionList.as_view(), name='transaction-list'),
    path('<int:pk>/', views.TransactionDetail.as_view(), name='transaction-detail'),
    path('', views.TransactionClosing.as_view(), name='transaction-closing'),

]

urlpatterns += [
    path('api-auth', include('rest_framework.urls')),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
