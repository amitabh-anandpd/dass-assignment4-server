from django.contrib import admin

from .models import Exam, ExamReport, Grade


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'batch', 'subject', 'exam_type', 'evaluation_method', 'is_published')
    search_fields = ('title', 'course__code', 'subject__code')


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('exam', 'student', 'marks_obtained', 'grade_letter', 'grade_points')
    search_fields = ('student__username', 'exam__title')


@admin.register(ExamReport)
class ExamReportAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'exam', 'course', 'batch', 'generated_by', 'generated_at')
    search_fields = ('exam__title', 'course__code', 'batch__code')