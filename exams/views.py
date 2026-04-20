from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Exam, ExamReport, Grade
from .serializers import ExamReportSerializer, ExamSerializer, GradeSerializer


@api_view(['GET', 'POST'])
def exams_list_create(request):
    if request.method == 'GET':
        queryset = Exam.objects.select_related('course', 'batch', 'subject', 'parent_exam').all().order_by('id')
        return Response(ExamSerializer(queryset, many=True).data)

    serializer = ExamSerializer(data=request.data)
    if serializer.is_valid():
        item = serializer.save()
        return Response(ExamSerializer(item).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def exams_detail(request, pk):
    item = get_object_or_404(Exam, pk=pk)

    if request.method == 'GET':
        return Response(ExamSerializer(item).data)

    if request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = ExamSerializer(item, data=request.data, partial=partial)
        if serializer.is_valid():
            item = serializer.save()
            return Response(ExamSerializer(item).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def grades_list_create(request):
    if request.method == 'GET':
        queryset = Grade.objects.select_related('exam', 'student').all().order_by('id')
        return Response(GradeSerializer(queryset, many=True).data)

    serializer = GradeSerializer(data=request.data)
    if serializer.is_valid():
        item = serializer.save()
        return Response(GradeSerializer(item).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def grades_detail(request, pk):
    item = get_object_or_404(Grade, pk=pk)

    if request.method == 'GET':
        return Response(GradeSerializer(item).data)

    if request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = GradeSerializer(item, data=request.data, partial=partial)
        if serializer.is_valid():
            item = serializer.save()
            return Response(GradeSerializer(item).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def exam_reports_list_create(request):
    if request.method == 'GET':
        queryset = ExamReport.objects.select_related('exam', 'course', 'batch', 'generated_by').all().order_by('id')
        return Response(ExamReportSerializer(queryset, many=True).data)

    serializer = ExamReportSerializer(data=request.data)
    if serializer.is_valid():
        item = serializer.save()
        return Response(ExamReportSerializer(item).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def exam_reports_detail(request, pk):
    item = get_object_or_404(ExamReport, pk=pk)

    if request.method == 'GET':
        return Response(ExamReportSerializer(item).data)

    if request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = ExamReportSerializer(item, data=request.data, partial=partial)
        if serializer.is_valid():
            item = serializer.save()
            return Response(ExamReportSerializer(item).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)