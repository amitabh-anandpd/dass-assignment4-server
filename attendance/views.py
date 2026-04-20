from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Attendance
from .serializers import AttendanceSerializer


@api_view(['GET', 'POST'])
def attendance_records_list_create(request):
    if request.method == 'GET':
        queryset = Attendance.objects.select_related('student', 'enrollment', 'course', 'batch', 'subject', 'marked_by').all().order_by('id')
        return Response(AttendanceSerializer(queryset, many=True).data)

    serializer = AttendanceSerializer(data=request.data)
    if serializer.is_valid():
        item = serializer.save()
        return Response(AttendanceSerializer(item).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def attendance_records_detail(request, pk):
    item = get_object_or_404(Attendance, pk=pk)

    if request.method == 'GET':
        return Response(AttendanceSerializer(item).data)

    if request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = AttendanceSerializer(item, data=request.data, partial=partial)
        if serializer.is_valid():
            item = serializer.save()
            return Response(AttendanceSerializer(item).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)