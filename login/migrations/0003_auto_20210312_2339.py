# Generated by Django 3.1.7 on 2021-03-12 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20210214_1321'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='email',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='staff',
            name='fname',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='staff',
            name='img',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='staff',
            name='lname',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]