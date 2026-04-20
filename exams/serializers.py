from rest_framework import serializers

from .models import Exam, ExamReport, Grade


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'


class ExamReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamReport
        fields = '__all__'