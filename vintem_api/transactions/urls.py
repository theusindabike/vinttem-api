from django.urls import path, include
from . import views

app_name = 'transactions'

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.transactions_list),
]
