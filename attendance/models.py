from django.conf import settings
from django.db import models

from academics.models import Batch, Course, Enrollment, Subject


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Attendance(TimestampedModel):
    class Status(models.TextChoices):
        PRESENT = 'present', 'Present'
        ABSENT = 'absent', 'Absent'
        LATE = 'late', 'Late'
        EXCUSED = 'excused', 'Excused'

    class ReportType(models.TextChoices):
        DAILY = 'daily', 'Daily'
        MONTHLY = 'monthly', 'Monthly'
        SUBJECT_WISE = 'subject_wise', 'Subject wise'

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendance_records')
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='attendance_records', null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendance_records')
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True, related_name='attendance_records')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='attendance_records')
    attendance_date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PRESENT)
    report_type = models.CharField(max_length=20, choices=ReportType.choices, default=ReportType.DAILY)
    remarks = models.TextField(blank=True)
    marked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='marked_attendance')

    class Meta:
        unique_together = ('student', 'course', 'attendance_date', 'subject')

    def __str__(self):
        return f'{self.student_id} - {self.attendance_date}'