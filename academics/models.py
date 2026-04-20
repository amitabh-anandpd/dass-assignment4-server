from django.conf import settings
from django.db import models


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class StudentCategory(TimestampedModel):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    allows_graduation = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Course(TimestampedModel):
    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.code} - {self.name}'


class Batch(TimestampedModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='batches')
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=200)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('course', 'code')

    def __str__(self):
        return f'{self.course.code} / {self.code}'


class Subject(TimestampedModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects')
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=200)
    is_elective = models.BooleanField(default=False)
    credits = models.DecimalField(max_digits=4, decimal_places=1, default=0)

    class Meta:
        unique_together = ('course', 'code')

    def __str__(self):
        return f'{self.course.code} / {self.code}'


class Enrollment(TimestampedModel):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        TRANSFERRED = 'transferred', 'Transferred'
        COMPLETED = 'completed', 'Completed'
        DROPPED = 'dropped', 'Dropped'

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True, related_name='enrollments')
    category = models.ForeignKey(StudentCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='enrollments')
    admission_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    joined_on = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f'{self.student_id} - {self.course.code}'


class BatchTransfer(TimestampedModel):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='batch_transfers')
    from_batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='transfers_from')
    to_batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='transfers_to')
    transferred_on = models.DateField()
    reason = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f'{self.enrollment_id}: {self.from_batch_id} -> {self.to_batch_id}'