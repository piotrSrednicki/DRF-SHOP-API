import base64

from django.contrib.auth import get_user_model, authenticate
from django.core import validators
from django.core.exceptions import ValidationError
from datetime import datetime
from django.conf import settings
from django.db import models
from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.permissions import BasePermission


def get_authorization_header(request):
    auth = request.META.get("HTTP_AUTHORIZATION", "")
    return auth


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


class CustomUserAuthentication(authentication.BasicAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != "basic":
            return None

        if len(auth) == 1:
            raise exceptions.AuthenticationFailed("Invalid basic header. No credentials provided.")
        if len(auth) > 2:
            raise exceptions.AuthenticationFailed("Invalid basic header. Credential string is not properly formatted")
        try:
            auth_decoded = base64.b64decode(auth[1]).decode("utf-8")
            username, password = auth_decoded.split(":")
        except (UnicodeDecodeError, ValueError):
            raise exceptions.AuthenticationFailed("Invalid basic header. Credentials not correctly encoded")

        return self.authenticate_credentials(username, password, request)

    def authenticate_credentials(self, username, password, request=None):
        user = get_user_model().objects.filter(username=username)[0]
        if user.username != username or user.password != password:
            raise exceptions.AuthenticationFailed("Invalid username or password")

        return user, None
