# Generated by Django 3.1.7 on 2021-03-18 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0010_remove_staff_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='email',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='staff',
            name='fname',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='staff',
            name='img',
            field=models.ImageField(upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='lname',
            field=models.CharField(max_length=100),
        ),
    ]
