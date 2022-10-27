from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    pass


def __str__(self):
    return self.name
