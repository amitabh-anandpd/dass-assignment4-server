from django.urls import path

from .views import requested_reports_detail, requested_reports_list_create

urlpatterns = [
	path('requested-reports/', requested_reports_list_create, name='requested_reports_list_create'),
	path('requested-reports/<int:pk>/', requested_reports_detail, name='requested_reports_detail'),
]