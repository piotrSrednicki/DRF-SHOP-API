from rest_framework import serializers
from .models import *


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class IntegerListField(serializers.Field):
    def to_representation(self, obj):
        return [int(x) for x in obj.split(',')]

    def to_internal_value(self, data):
        return ','.join(str(x) for x in data.split(','))


class OrderSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=7, decimal_places=2, read_only=True)
    productsCounts = IntegerListField()

    class Meta:
        model = Order
        fields = ['id', 'client', 'address', 'products', 'date', 'paymentDate', 'price', 'productsCounts', ]

    def create(self, data):
        products = Product.objects.all()
        order = Order.objects.create(client=data['client'], address=data['address'], date=data['date'],
                                     paymentDate=data['paymentDate'], )
        pks = []
        for product in products:
            pks.append(product.name)
        for product in products:
            if product.pk in pks:
                order.products.add(product)
        return change_price(data, order)

    def update(self, instance, data):
        updatedOrder = super().update(instance, data)
        return change_price(data, updatedOrder)


def change_price(data, order):
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

    picture = data.get('picture', None)
    miniaturePicture = Image.open(picture)
    miniaturePicture = miniaturePicture.resize((200, 200))
    miniaturePicture.save(picture.path)
    order.miniaturePicture = miniaturePicture
    order.price = price
    order.productsCounts = productsCounts
    order.save()
    return order
