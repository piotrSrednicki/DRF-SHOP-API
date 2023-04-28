from django.core import validators
from django.core.exceptions import ValidationError
from datetime import datetime
from django.conf import settings
from django.db import models
from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group

def validate_image_size(image):
    img = Image.open(image)
    width, height = img.size
    if width > 200 or height > 200:
        raise ValidationError(f"Max image size is 200x200. The uploaded picture is {width}x{height}.")


class CustomUser(AbstractUser):
    role = models.CharField(max_length=50)


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    description = models.CharField(max_length=300)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='pictures/')
    miniaturePicture = models.ImageField(upload_to='miniatures/', validators=[validate_image_size], null=True,
                                         editable=False)

    def __str__(self):
        return self.name


class Order(models.Model):
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    products = models.ManyToManyField(Product)
    productsCounts = models.CharField(max_length=100, validators=[validators.validate_comma_separated_integer_list],
                                      null=True)
    date = models.DateTimeField(default=datetime.today)
    paymentDate = models.DateTimeField()
    price = models.DecimalField(decimal_places=2, max_digits=7, null=True, editable=False)

    def __str__(self):
        return self.client.__str__() + " " + str(self.price)
