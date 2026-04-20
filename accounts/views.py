from django.contrib.auth import get_user_model
from rest_framework import viewsets

from .models import Configuration, SystemConfiguration
from .serializers import ConfigurationSerializer, SystemConfigurationSerializer, UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer


class ConfigurationViewSet(viewsets.ModelViewSet):
    queryset = Configuration.objects.select_related('user').all().order_by('id')
    serializer_class = ConfigurationSerializer


class SystemConfigurationViewSet(viewsets.ModelViewSet):
    queryset = SystemConfiguration.objects.all().order_by('id')
    serializer_class = SystemConfigurationSerializer