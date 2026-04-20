from django.db import models


class ReportRequest(models.Model):
    class ReportKind(models.TextChoices):
        EXAM = 'exam', 'Exam'
        ATTENDANCE = 'attendance', 'Attendance'
        ACADEMIC = 'academic', 'Academic'

    title = models.CharField(max_length=200)
    report_kind = models.CharField(max_length=20, choices=ReportKind.choices)
    parameters = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title