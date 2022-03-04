from django.db import models

# Create your models here.
class Account(models.Model):
    accountUrl = models.CharField(max_length=50)
    avatar = models.CharField(max_length=255, null=True, default="")
    level = models.CharField(max_length=2)
    def __str__(self):
        return f'{self.accountUrl}, {self.level}, {self.level}'

