from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Configuration, SystemConfiguration
from .serializers import ConfigurationSerializer, SystemConfigurationSerializer, UserSerializer

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    identifier = (
        request.data.get('username')
        or request.data.get('email')
        or request.data.get('identifier')
    )
    password = request.data.get('password')

    if not identifier or not password:
        return Response(
            {'detail': 'username/email and password are required.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    identifier = identifier.strip()

    username = identifier
    if '@' in identifier:
        user_obj = User.objects.filter(email__iexact=identifier).first()
        if user_obj:
            username = user_obj.username

    user = authenticate(request, username=username, password=password)

    # Fallback path for deployments where backend auth resolution differs.
    if not user:
        candidate = User.objects.filter(
            Q(username__iexact=identifier) | Q(email__iexact=identifier)
        ).first()
        if candidate and candidate.check_password(password):
            user = candidate

    if not user:
        return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

    if not user.is_active:
        return Response({'detail': 'User account is inactive.'}, status=status.HTTP_403_FORBIDDEN)

    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return Response({'detail': 'Login successful.', 'user_id': user.id, 'username': user.username}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def users_list_create(request):
    if request.method == 'GET':
        queryset = User.objects.all().order_by('id')
        return Response(UserSerializer(queryset, many=True).data)

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def users_detail(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'GET':
        return Response(UserSerializer(user).data)

    if request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = UserSerializer(user, data=request.data, partial=partial)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def configurations_list_create(request):
    if request.method == 'GET':
        queryset = Configuration.objects.select_related('user').all().order_by('id')
        return Response(ConfigurationSerializer(queryset, many=True).data)

    serializer = ConfigurationSerializer(data=request.data)
    if serializer.is_valid():
        item = serializer.save()
        return Response(ConfigurationSerializer(item).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def configurations_detail(request, pk):
    item = get_object_or_404(Configuration, pk=pk)

    if request.method == 'GET':
        return Response(ConfigurationSerializer(item).data)

    if request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = ConfigurationSerializer(item, data=request.data, partial=partial)
        if serializer.is_valid():
            item = serializer.save()
            return Response(ConfigurationSerializer(item).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def system_configurations_list_create(request):
    if request.method == 'GET':
        queryset = SystemConfiguration.objects.all().order_by('id')
        return Response(SystemConfigurationSerializer(queryset, many=True).data)

    serializer = SystemConfigurationSerializer(data=request.data)
    if serializer.is_valid():
        item = serializer.save()
        return Response(SystemConfigurationSerializer(item).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def system_configurations_detail(request, pk):
    item = get_object_or_404(SystemConfiguration, pk=pk)

    if request.method == 'GET':
        return Response(SystemConfigurationSerializer(item).data)

    if request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = SystemConfigurationSerializer(item, data=request.data, partial=partial)
        if serializer.is_valid():
            item = serializer.save()
            return Response(SystemConfigurationSerializer(item).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)