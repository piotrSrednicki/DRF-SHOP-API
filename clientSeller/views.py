from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.


class AllModelsAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    currentModel = None
    currentSerializer = None

    def __init__(self, currentModel, currentSerializer):
        super().__init__()
        self.currentModel: models.Model.__class__ = currentModel
        self.currentSerializer: serializers.ModelSerializer.__class__ = currentSerializer

    def get(self, request):
        currentObjects = self.currentModel.objects.all()
        serializer = self.currentSerializer(currentObjects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.currentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllModelsDetailsAPIView(APIView):
    currentModel = None
    currentSerializer = None

    def __init__(self, currentModel, currentSerializer):
        super().__init__()
        self.currentModel: models.Model.__class__ = currentModel
        self.currentSerializer: serializers.ModelSerializer.__class__ = currentSerializer

    def get_object(self, pk):
        try:
            if self.currentModel in [Product, ProductCategory]:
                return self.currentModel.objects.get(name=pk)
            else:
                return self.currentModel.objects.get(pk=pk)

        except self.currentModel.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, name):
        currentObject = self.get_object(name)
        serializer = self.currentSerializer(currentObject)
        try:
            return Response(serializer.data)
        except AttributeError:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, name):
        currentObject = self.get_object(name)
        serializer = self.currentSerializer(currentObject, data=request.data)
        try:
            if serializer.is_valid():
                currentObject.delete()
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AttributeError:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, name):
        try:
            currentObject = self.get_object(name)
            currentObject.delete()
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        except AttributeError:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def product_category_list(request):
    if request.method == 'GET':
        productCategories = ProductCategory.objects.all()
        serializer = ProductCategorySerializer(productCategories, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def order_list(request):
    if request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def product_category_detail(request, name: str):
    try:
        productCategory = ProductCategory.objects.get(name=name)

    except ProductCategory.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductCategorySerializer(productCategory)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductCategorySerializer(productCategory, data=request.data)
        if serializer.is_valid():
            productCategory.delete()
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        productCategory.delete()
        return HttpResponse(status=204)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, name: str):
    try:
        product = Product.objects.get(name=name)

    except Product.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            product.delete()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        product.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def order_detail(request, pk: int):
    try:
        order = Order.objects.get(pk=pk)

    except Order.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            order.delete()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        order.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
