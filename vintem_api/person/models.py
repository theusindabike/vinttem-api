from django.db import models
from rest_framework import serializers


class Person(models.Model):
    name = models.CharField('nome', max_length=127)
    email = models.EmailField('email')
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    last_login = models.DateTimeField('último login', blank=True)


def __str__(self):
    return self.name
