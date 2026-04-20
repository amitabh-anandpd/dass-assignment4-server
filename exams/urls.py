from django.urls import path

from .views import (
	exam_reports_detail,
	exam_reports_list_create,
	exams_detail,
	exams_list_create,
	grades_detail,
	grades_list_create,
)

urlpatterns = [
	path('exams/', exams_list_create, name='exams_list_create'),
	path('exams/<int:pk>/', exams_detail, name='exams_detail'),
	path('grades/', grades_list_create, name='grades_list_create'),
	path('grades/<int:pk>/', grades_detail, name='grades_detail'),
	path('exam-reports/', exam_reports_list_create, name='exam_reports_list_create'),
	path('exam-reports/<int:pk>/', exam_reports_detail, name='exam_reports_detail'),
]