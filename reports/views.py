from rest_framework import viewsets

from .models import ReportRequest
from .serializers import ReportRequestSerializer


class ReportRequestViewSet(viewsets.ModelViewSet):
    queryset = ReportRequest.objects.all().order_by('id')
    serializer_class = ReportRequestSerializer