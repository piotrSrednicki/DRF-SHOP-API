from datetime import datetime
from django.conf import settings
from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    description = models.CharField(max_length=300)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    picture = models.ImageField()
    miniaturePicture = models.ImageField()

    def __str__(self):
        return self.name


class Order(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    products = models.ManyToManyField(Product)
    date = models.DateTimeField(default=datetime.today())
    paymentDate = models.DateTimeField()
    price = models.DecimalField(decimal_places=2, max_digits=5)

    def __str__(self):
        return self.products.__str__()
