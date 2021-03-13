from django.db import models

# Create your models here.


class Staff(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=100, blank=True)
    fname = models.CharField(max_length=100,  blank=True)
    lname = models.CharField(max_length=100,  blank=True)
    passwrd = models.CharField(max_length=100)
    img = models.ImageField(upload_to='media/',  blank=True)
    is_email_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.email}'


class Password(models.Model):
    user = models.ForeignKey(Staff, on_delete=models.CASCADE)
    app_name = models.CharField(max_length=100)
    app_email = models.CharField(max_length=100)
    app_password = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.app_name}'
