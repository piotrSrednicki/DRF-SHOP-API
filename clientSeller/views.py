from django.http import HttpResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import BasePermission


class ListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserRolePermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'user':
            return True
        else:
            return False


class SellerRolePermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'seller':
            return True
        else:
            return False


class AllModelsAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    pagination_class = ListPagination
    currentModel = None
    currentSerializer = None

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = []
        elif self.request.method == 'POST':
            permission_classes = [SellerRolePermission]
        else:
            permission_classes = [SellerRolePermission]
        return [permission() for permission in permission_classes]

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
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    pagination_class = ListPagination
    currentModel = None
    currentSerializer = None

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = []
        elif self.request.method == 'PUT':
            permission_classes = [SellerRolePermission]
        elif self.request.method == 'DELETE':
            permission_classes = [SellerRolePermission]
        else:
            permission_classes = [SellerRolePermission]
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
