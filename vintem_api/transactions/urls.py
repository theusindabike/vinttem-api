from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'transactions'

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.TransactionList.as_view()),
    path('<int:pk>/', views.TransactionDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
]

urlpatterns += [
    path('api-auth', include('rest_framework.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
