# Generated by Django 3.1.7 on 2021-03-17 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0009_auto_20210316_0046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='username',
        ),
    ]