from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Batch, BatchTransfer, Course, Enrollment, StudentCategory, Subject
from .serializers import (
    BatchSerializer,
    BatchTransferSerializer,
    CourseSerializer,
    EnrollmentSerializer,
    StudentCategorySerializer,
    SubjectSerializer,
)


@api_view(['GET', 'POST'])
def student_categories_list_create(request):
    if request.method == 'GET':
        queryset = StudentCategory.objects.all().order_by('id')
        return Response(StudentCategorySerializer(queryset, many=True).data)

    serializer = StudentCategorySerializer(data=request.data)
    if serializer.is_valid():
        item = serializer.save()
        return Response(StudentCategorySerializer(item).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def student_categories_detail(request, pk):
    item = get_object_or_404(StudentCategory, pk=pk)

    if request.method == 'GET':
        return Response(StudentCategorySerializer(item).data)

    if request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = StudentCategorySerializer(item, data=request.data, partial=partial)
        if serializer.is_valid():
            item = serializer.save()
            return Response(StudentCategorySerializer(item).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def courses_list_create(request):
    if request.method == 'GET':
        queryset = Course.objects.all().order_by('id')
        return Response(CourseSerializer(queryset, many=True).data)

    serializer = CourseSerializer(data=request.data)
    if serializer.is_valid():
        item = serializer.save()
        return Response(CourseSerializer(item).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def courses_detail(request, pk):
    item = get_object_or_404(Course, pk=pk)

    if request.method == 'GET':
        return Response(CourseSerializer(item).data)

    if request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = CourseSerializer(item, data=request.data, partial=partial)
        if serializer.is_valid():
            item = serializer.save()
            return Response(CourseSerializer(item).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def batches_list_create(request):
    if request.method == 'GET':
        queryset = Batch.objects.select_related('course').all().order_by('id')
        return Response(BatchSerializer(queryset, many=True).data)

    serializer = BatchSerializer(data=request.data)
    if serializer.is_valid():
        item = serializer.save()
        return Response(BatchSerializer(item).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def batches_detail(request, pk):
    item = get_object_or_404(Batch, pk=pk)

    if request.method == 'GET':
        return Response(BatchSerializer(item).data)

    if request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = BatchSerializer(item, data=request.data, partial=partial)
        if serializer.is_valid():
            item = serializer.save()
            return Response(BatchSerializer(item).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def subjects_list_create(request):
    if request.method == 'GET':
        queryset = Subject.objects.select_related('course').all().order_by('id')
        return Response(SubjectSerializer(queryset, many=True).data)

    serializer = SubjectSerializer(data=request.data)
    if serializer.is_valid():
        item = serializer.save()
        return Response(SubjectSerializer(item).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def subjects_detail(request, pk):
    item = get_object_or_404(Subject, pk=pk)

    if request.method == 'GET':
        return Response(SubjectSerializer(item).data)

    if request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = SubjectSerializer(item, data=request.data, partial=partial)
        if serializer.is_valid():
            item = serializer.save()
            return Response(SubjectSerializer(item).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def enrollments_list_create(request):
    if request.method == 'GET':
        queryset = Enrollment.objects.select_related('student', 'course', 'batch', 'category').all().order_by('id')
        return Response(EnrollmentSerializer(queryset, many=True).data)

    serializer = EnrollmentSerializer(data=request.data)
    if serializer.is_valid():
        item = serializer.save()
        return Response(EnrollmentSerializer(item).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def enrollments_detail(request, pk):
    item = get_object_or_404(Enrollment, pk=pk)

    if request.method == 'GET':
        return Response(EnrollmentSerializer(item).data)

    if request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = EnrollmentSerializer(item, data=request.data, partial=partial)
        if serializer.is_valid():
            item = serializer.save()
            return Response(EnrollmentSerializer(item).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def batch_transfers_list_create(request):
    if request.method == 'GET':
        queryset = BatchTransfer.objects.select_related('enrollment', 'from_batch', 'to_batch').all().order_by('id')
        return Response(BatchTransferSerializer(queryset, many=True).data)

    serializer = BatchTransferSerializer(data=request.data)
    if serializer.is_valid():
        item = serializer.save()
        return Response(BatchTransferSerializer(item).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def batch_transfers_detail(request, pk):
    item = get_object_or_404(BatchTransfer, pk=pk)

    if request.method == 'GET':
        return Response(BatchTransferSerializer(item).data)

    if request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = BatchTransferSerializer(item, data=request.data, partial=partial)
        if serializer.is_valid():
            item = serializer.save()
            return Response(BatchTransferSerializer(item).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)