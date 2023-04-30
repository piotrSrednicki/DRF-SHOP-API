import json

from django.http import HttpResponse, FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from .authentication import CustomUserAuthentication, SellerRolePermission, UserRolePermission
from .filters import ProductFilterSet
from .pagination import ListPagination
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from .models import *
from rest_framework.filters import OrderingFilter


class AllModelsAPIView(ListAPIView):
    pagination_class = ListPagination
    currentModel = None
    currentSerializer = None
    authentication_classes = [CustomUserAuthentication]

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = []
        elif self.request.method == 'POST':
            if self.currentModel == Order:
                permission_classes = [UserRolePermission]
            else:
                permission_classes = [SellerRolePermission]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def __init__(self, currentModel, currentSerializer):
        super().__init__()
        self.currentModel: models.Model.__class__ = currentModel
        self.currentSerializer: serializers.ModelSerializer.__class__ = currentSerializer
        self.serializer_class = currentSerializer
        if self.currentModel == Product:
            self.filter_class = ProductFilterSet
            self.filter_backends = [DjangoFilterBackend, OrderingFilter]
            self.filterset_class = ProductFilterSet
            self.ordering_fields = ['name', 'price', 'category']

    def get_queryset(self):
        return self.currentModel.objects.all()

    def post(self, request):
        serializer = self.currentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllModelsDetailsAPIView(APIView):
    pagination_class = ListPagination
    currentModel = None
    currentSerializer = None
    authentication_classes = [CustomUserAuthentication]

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = []
        elif self.request.method == 'PUT':
            permission_classes = [SellerRolePermission]
        elif self.request.method == 'DELETE':
            permission_classes = [SellerRolePermission]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

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

    def get(self, request, pk):
        currentObject = self.get_object(pk)
        serializer = self.currentSerializer(currentObject)
        try:
            return Response(serializer.data)
        except AttributeError:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        currentObject = self.get_object(pk)
        serializer = self.currentSerializer(currentObject, data=request.data)
        try:
            if serializer.is_valid():
                currentObject.delete()
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AttributeError:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            currentObject = self.get_object(pk)
            currentObject.delete()
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        except AttributeError:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)


class StatisticsAPIView(APIView):
    pagination_class = ListPagination
    authentication_classes = [CustomUserAuthentication]

    def get_permissions(self):
        permission_classes = [SellerRolePermission]
        return [permission() for permission in permission_classes]

    def get(self, request):
        serializer = ProductStatisticsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dateFrom = serializer.validated_data['dateFrom']
        dateTo = serializer.validated_data['dateTo']
        lengthOfTopSellingList = serializer.validated_data['lengthOfTopSellingList']
        products = Product.objects.filter()
        productsWithCounts: list = []
        for product in products:
            productsWithCounts.append(dict({"name": product.name,
                                            "description": product.description,
                                            "price": float(product.price),
                                            "category": product.category.name,
                                            "picture": str(product.picture),
                                            "miniaturePicture": str(product.miniaturePicture),
                                            "count": 0}))
        orders = Order.objects.filter(date__range=[dateFrom, dateTo])
        for order in orders:
            for orderProductindex, orderProduct in enumerate(order.products.all()):
                for productIndex, product in enumerate(products):
                    if orderProduct.name == product.name:
                        productsWithCounts[productIndex]["count"] += int(order.productsCounts[orderProductindex * 2])
        productsWithCountsSortedAndFiltered = sorted(productsWithCounts, key=lambda x: x['count'], reverse=True)
        if len(productsWithCountsSortedAndFiltered) > lengthOfTopSellingList:
            productsWithCountsSortedAndFiltered = productsWithCountsSortedAndFiltered[:lengthOfTopSellingList]
        productsWithCountsSortedAndFilteredJSON = json.dumps(productsWithCountsSortedAndFiltered, indent=4)
        return HttpResponse(productsWithCountsSortedAndFilteredJSON, status=status.HTTP_201_CREATED)


class PictureView(APIView):
    def get(self, request, path):
        try:
            image_file = open(f"pictures/{path}", "rb")
            return FileResponse(image_file)
        except FileNotFoundError:
            return Response({"message": "Image not found."}, status=status.HTTP_404_NOT_FOUND)


class MiniaturePictureView(APIView):
    def get(self, request, path):
        try:
            image_file = open(f"miniatures/{path}", "rb")
            return FileResponse(image_file)
        except FileNotFoundError:
            return Response({"message": "Image not found."}, status=status.HTTP_404_NOT_FOUND)
