from django.contrib import admin

from .models import Batch, BatchTransfer, Course, Enrollment, StudentCategory, Subject


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'is_active', 'updated_at')
    search_fields = ('code', 'name')


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'course', 'is_active')
    search_fields = ('code', 'name', 'course__code')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'course', 'is_elective')
    search_fields = ('code', 'name', 'course__code')


@admin.register(StudentCategory)
class StudentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'allows_graduation')
    search_fields = ('name',)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('admission_number', 'student', 'course', 'batch', 'status')
    search_fields = ('admission_number', 'student__username', 'course__code')


@admin.register(BatchTransfer)
class BatchTransferAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'from_batch', 'to_batch', 'transferred_on')
    search_fields = ('enrollment__admission_number', 'from_batch__code', 'to_batch__code')