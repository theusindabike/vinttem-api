# Generated by Django 4.1.2 on 2022-10-25 01:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='person',
            name='last_login',
        ),
    ]
