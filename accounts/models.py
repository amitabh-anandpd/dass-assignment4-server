from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'student', 'Student'
        ADMIN = 'admin', 'Admin'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    email = models.EmailField(unique=True)

    def save(self, *args, **kwargs):
        if self.role == self.Role.ADMIN:
            self.is_staff = True
        super().save(*args, **kwargs)


class Student(User):
    class Meta:
        proxy = True
        verbose_name = 'Student'
        verbose_name_plural = 'Students'


class Admin(User):
    class Meta:
        proxy = True
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'


class Configuration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='configuration')
    country = models.CharField(max_length=100, blank=True)
    currency = models.CharField(max_length=10, blank=True)
    time_zone = models.CharField(max_length=64, blank=True, default='UTC')
    language = models.CharField(max_length=16, blank=True, default='en')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} preferences'


class SystemConfiguration(models.Model):
    class GradingSystem(models.TextChoices):
        MARKS = 'marks', 'Marks'
        GPA = 'gpa', 'GPA'
        CCE = 'cce', 'CCE'
        CWA = 'cwa', 'CWA'
        CUSTOM = 'custom', 'Custom'

    grading_system = models.CharField(max_length=20, choices=GradingSystem.choices, default=GradingSystem.MARKS)
    auto_unique_ids = models.BooleanField(default=True)
    unique_id_prefix = models.CharField(max_length=20, blank=True)
    unique_id_padding = models.PositiveSmallIntegerField(default=4)
    default_country = models.CharField(max_length=100, blank=True)
    default_currency = models.CharField(max_length=10, blank=True)
    default_time_zone = models.CharField(max_length=64, blank=True, default='UTC')
    default_language = models.CharField(max_length=16, blank=True, default='en')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'System configuration'