from django.conf import settings
from django.db import models

from academics.models import Batch, Course, Subject


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Exam(TimestampedModel):
    class ExamType(models.TextChoices):
        MARKS = 'marks', 'Marks'
        GRADE = 'grade', 'Grade'
        CUSTOM = 'custom', 'Custom'

    class EvaluationMethod(models.TextChoices):
        GPA = 'gpa', 'GPA'
        CCE = 'cce', 'CCE'
        CWA = 'cwa', 'CWA'
        STANDARD = 'standard', 'Standard'

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True, related_name='exams')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='exams')
    title = models.CharField(max_length=200)
    exam_type = models.CharField(max_length=20, choices=ExamType.choices, default=ExamType.MARKS)
    evaluation_method = models.CharField(max_length=20, choices=EvaluationMethod.choices, default=EvaluationMethod.STANDARD)
    group_name = models.CharField(max_length=120, blank=True)
    parent_exam = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='child_exams')
    max_marks = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    passing_marks = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    scheduled_on = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Grade(TimestampedModel):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='grades')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='grades')
    marks_obtained = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    grade_letter = models.CharField(max_length=10, blank=True)
    grade_points = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    remarks = models.TextField(blank=True)

    class Meta:
        unique_together = ('exam', 'student')

    def __str__(self):
        return f'{self.student_id} / {self.exam_id}'


class ExamReport(TimestampedModel):
    class ReportType(models.TextChoices):
        AUTOMATED = 'automated', 'Automated'
        QUICK = 'quick', 'Quick'
        ON_DEMAND = 'on_demand', 'On demand'

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='reports', null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reports', null=True, blank=True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='reports', null=True, blank=True)
    report_type = models.CharField(max_length=20, choices=ReportType.choices, default=ReportType.ON_DEMAND)
    generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='generated_exam_reports')
    summary = models.TextField(blank=True)
    payload = models.JSONField(default=dict, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.report_type} report #{self.pk}'