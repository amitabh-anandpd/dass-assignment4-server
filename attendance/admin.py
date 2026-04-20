from django.contrib import admin

from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'batch', 'subject', 'attendance_date', 'status', 'report_type')
    search_fields = ('student__username', 'course__code', 'subject__code')