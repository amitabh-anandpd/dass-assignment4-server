from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Configuration, SystemConfiguration

User = get_user_model()


class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class SystemConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemConfiguration
        fields = '__all__'
        read_only_fields = ('updated_at',)


class UserSerializer(serializers.ModelSerializer):
    configuration = ConfigurationSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'configuration')
        read_only_fields = ('id',)