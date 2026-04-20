from django.urls import path

from .views import (
	configurations_detail,
	configurations_list_create,
	login_user,
	signup,
	system_configurations_detail,
	system_configurations_list_create,
	users_detail,
	users_list_create,
)

urlpatterns = [
	path('signup/', signup, name='signup'),
	path('login/', login_user, name='login'),
	path('users/', users_list_create, name='users_list_create'),
	path('users/<int:pk>/', users_detail, name='users_detail'),
	path('configurations/', configurations_list_create, name='configurations_list_create'),
	path('configurations/<int:pk>/', configurations_detail, name='configurations_detail'),
	path('system-configurations/', system_configurations_list_create, name='system_configurations_list_create'),
	path('system-configurations/<int:pk>/', system_configurations_detail, name='system_configurations_detail'),
]