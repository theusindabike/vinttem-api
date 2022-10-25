from django.db import models
from rest_framework import serializers


class Person(models.Model):
    name = models.CharField('nome', max_length=127)
    email = models.EmailField('email')


def __str__(self):
    return self.name
