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
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'password', 'configuration')
        read_only_fields = ('id',)
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user