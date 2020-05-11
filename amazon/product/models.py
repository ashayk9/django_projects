from django.db import models

# Create your models here.


class Product(models.Model):
    title=models.CharField(max_length=200)
    price = models.DecimalField(max_digits=100 , decimal_places=2)
    description = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=False, null=True)