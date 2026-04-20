from rest_framework import viewsets

from .models import Batch, BatchTransfer, Course, Enrollment, StudentCategory, Subject
from .serializers import (
    BatchSerializer,
    BatchTransferSerializer,
    CourseSerializer,
    EnrollmentSerializer,
    StudentCategorySerializer,
    SubjectSerializer,
)


class StudentCategoryViewSet(viewsets.ModelViewSet):
    queryset = StudentCategory.objects.all().order_by('id')
    serializer_class = StudentCategorySerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('id')
    serializer_class = CourseSerializer


class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.select_related('course').all().order_by('id')
    serializer_class = BatchSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.select_related('course').all().order_by('id')
    serializer_class = SubjectSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.select_related('student', 'course', 'batch', 'category').all().order_by('id')
    serializer_class = EnrollmentSerializer


class BatchTransferViewSet(viewsets.ModelViewSet):
    queryset = BatchTransfer.objects.select_related('enrollment', 'from_batch', 'to_batch').all().order_by('id')
    serializer_class = BatchTransferSerializer