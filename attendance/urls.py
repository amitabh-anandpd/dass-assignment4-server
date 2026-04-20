from django.urls import path

from .views import attendance_records_detail, attendance_records_list_create

urlpatterns = [
	path('attendance-records/', attendance_records_list_create, name='attendance_records_list_create'),
	path('attendance-records/<int:pk>/', attendance_records_detail, name='attendance_records_detail'),
]