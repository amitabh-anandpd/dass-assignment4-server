from rest_framework import viewsets

from .models import Exam, ExamReport, Grade
from .serializers import ExamReportSerializer, ExamSerializer, GradeSerializer


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.select_related('course', 'batch', 'subject', 'parent_exam').all().order_by('id')
    serializer_class = ExamSerializer


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.select_related('exam', 'student').all().order_by('id')
    serializer_class = GradeSerializer


class ExamReportViewSet(viewsets.ModelViewSet):
    queryset = ExamReport.objects.select_related('exam', 'course', 'batch', 'generated_by').all().order_by('id')
    serializer_class = ExamReportSerializer