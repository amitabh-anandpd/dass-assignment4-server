from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ReportRequest
from .serializers import ReportRequestSerializer


@api_view(['GET', 'POST'])
def requested_reports_list_create(request):
    if request.method == 'GET':
        queryset = ReportRequest.objects.all().order_by('id')
        return Response(ReportRequestSerializer(queryset, many=True).data)

    serializer = ReportRequestSerializer(data=request.data)
    if serializer.is_valid():
        item = serializer.save()
        return Response(ReportRequestSerializer(item).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def requested_reports_detail(request, pk):
    item = get_object_or_404(ReportRequest, pk=pk)

    if request.method == 'GET':
        return Response(ReportRequestSerializer(item).data)

    if request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = ReportRequestSerializer(item, data=request.data, partial=partial)
        if serializer.is_valid():
            item = serializer.save()
            return Response(ReportRequestSerializer(item).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)