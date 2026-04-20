from django.urls import path

from .views import (
	batch_transfers_detail,
	batch_transfers_list_create,
	batches_detail,
	batches_list_create,
	courses_detail,
	courses_list_create,
	enrollments_detail,
	enrollments_list_create,
	student_categories_detail,
	student_categories_list_create,
	subjects_detail,
	subjects_list_create,
)

urlpatterns = [
	path('student-categories/', student_categories_list_create, name='student_categories_list_create'),
	path('student-categories/<int:pk>/', student_categories_detail, name='student_categories_detail'),
	path('courses/', courses_list_create, name='courses_list_create'),
	path('courses/<int:pk>/', courses_detail, name='courses_detail'),
	path('batches/', batches_list_create, name='batches_list_create'),
	path('batches/<int:pk>/', batches_detail, name='batches_detail'),
	path('subjects/', subjects_list_create, name='subjects_list_create'),
	path('subjects/<int:pk>/', subjects_detail, name='subjects_detail'),
	path('enrollments/', enrollments_list_create, name='enrollments_list_create'),
	path('enrollments/<int:pk>/', enrollments_detail, name='enrollments_detail'),
	path('batch-transfers/', batch_transfers_list_create, name='batch_transfers_list_create'),
	path('batch-transfers/<int:pk>/', batch_transfers_detail, name='batch_transfers_detail'),
]