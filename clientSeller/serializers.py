import base64
from datetime import timedelta

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import IntegerField

from .models import *
from django.core.mail import send_mail


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def create(self, data):
        product = Product.objects.create(**data)
        picture = data.get('picture', None)
        print(picture)
        miniaturePicture = Image.open(picture)
        miniaturePicture = miniaturePicture.resize((200, 200))
        print(miniaturePicture)
        product.miniaturePicture = "miniatures/"+product.name+".jpg"
        miniaturePicture.save("miniatures/"+product.name+".jpg")
        if not product.picture._committed:
            product.picture.save()
        product.save()
        return product

    def update(self, instance, data):
        updatedProduct = super().update(instance, data)
        picture = data.get('picture', None)
        miniaturePicture = Image.open(picture)
        print(picture)
        miniaturePicture = miniaturePicture.resize((200, 200))
        print(miniaturePicture)
        updatedProduct.miniaturePicture = "miniatures/"+updatedProduct.name+".jpg"
        miniaturePicture.save("miniatures/"+updatedProduct.name+".jpg")
        if not updatedProduct.picture._committed:
            updatedProduct.picture.save()
        updatedProduct.save()
        return updatedProduct


class IntegerListField(serializers.Field):
    def to_representation(self, obj):
        return [int(x) for x in obj.split(',')]

    def to_internal_value(self, data):
        return ','.join(str(x) for x in data.split(','))


class OrderSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=7, decimal_places=2, read_only=True)
    productsCounts = IntegerListField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'address', 'products', 'date', 'paymentDate', 'price', 'productsCounts', 'first_name',
                  'last_name']

    def get_first_name(self, obj):
        data = self.context.get('request').data
        first_name = data.get('first_name', None)
        return first_name

    def get_last_name(self, obj):
        data = self.context.get('request').data
        last_name = data.get('last_name', None)
        return last_name

    def get_non_model_data(self):
        data = self.context.get('request').data
        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)
        return {'first_name': first_name, 'last_name': last_name}

    def create(self, data):
        credentials = self.context.get('request').headers['Authorization']
        products = Product.objects.all()
        auth = credentials.split()
        print(data)
        try:
            auth_bytes = base64.b64decode(auth[1])
        except TypeError:
            return None
        credentials = auth_bytes.decode('utf-8').split(':')
        username = credentials[0]
        password = credentials[1]
        client = \
            get_user_model().objects.filter(username=username, password=password)[0]
        order = Order.objects.create(client=client, address=data['address'])
        pks = []
        for product in products:
            pks.append(product.name)
        for product in products:
            if product.pk in pks:
                order.products.add(product)
        return set_price_and_date(data, order)

    def update(self, instance, data):
        updatedOrder = super().update(instance, data)
        return set_price_and_date(data, updatedOrder)


def set_price_and_date(data, order):
    if len(data['products']) != len(str(data['productsCounts']).split(sep=',')):
        raise serializers.ValidationError("Amount of products is not equal to their respective counts. " +
                                          str(len(data['products'])) + "!=" +
                                          str(len(data['productsCounts'].split(','))))
    products = data.pop('products')
    price = 0
    productsCounts = data.pop('productsCounts')

    for currentIndex, product in enumerate(products):
        currentProduct = Product.objects.get(name=product.name)
        price += currentProduct.price * int(productsCounts.split(',')[currentIndex])

    order.price = price
    order.productsCounts = productsCounts
    order.date = datetime.today()
    order.paymentDate = datetime.today() + timedelta(days=5)
    order.save()
    try:
        send_mail(
            'An order has been created',
            f'Payment date: {order.paymentDate}, price: {order.price}, address: {order.address} ',
            'clientSeller@clientSeller.com',
            [str(order.client.email)],
            fail_silently=False,
        )
    except Exception as e:
        print("An email was not sent. Cause:", e)
    return order


class ProductStatisticsSerializer(serializers.Serializer):
    lengthOfTopSellingList = IntegerField(min_value=1)
    dateFrom = serializers.DateField()
    dateTo = serializers.DateField()

    class Meta:
        fields = ['lengthOfTopSellingList','dateFrom','dateTo']