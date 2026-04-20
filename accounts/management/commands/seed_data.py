from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from academics.models import Batch, BatchTransfer, Course, Enrollment, StudentCategory, Subject
from attendance.models import Attendance
from exams.models import Exam, ExamReport, Grade
from reports.models import ReportRequest
from accounts.models import Configuration, SystemConfiguration


class Command(BaseCommand):
    help = "Seed database with linked sample data (at least 2 rows per app table)."

    def handle(self, *args, **options):
        with transaction.atomic():
            self._seed_all()

        self.stdout.write(self.style.SUCCESS("Seeding complete."))

    def _seed_all(self):
        User = get_user_model()

        users = [
            self._upsert_user(
                User,
                username="admin001",
                email="admin001@example.com",
                password="Admin@12345",
                role=User.Role.ADMIN,
                first_name="Admin",
                last_name="One",
            ),
            self._upsert_user(
                User,
                username="admin002",
                email="admin002@example.com",
                password="Admin@12345",
                role=User.Role.ADMIN,
                first_name="Admin",
                last_name="Two",
            ),
            self._upsert_user(
                User,
                username="student001",
                email="student001@example.com",
                password="Student@12345",
                role=User.Role.STUDENT,
                first_name="Student",
                last_name="One",
            ),
            self._upsert_user(
                User,
                username="student002",
                email="student002@example.com",
                password="Student@12345",
                role=User.Role.STUDENT,
                first_name="Student",
                last_name="Two",
            ),
        ]

        student_users = [u for u in users if u.role == User.Role.STUDENT]
        admin_users = [u for u in users if u.role == User.Role.ADMIN]

        for idx, user in enumerate(users, start=1):
            Configuration.objects.get_or_create(
                user=user,
                defaults={
                    "country": "India",
                    "currency": "INR",
                    "time_zone": "Asia/Kolkata",
                    "language": "en",
                },
            )

        SystemConfiguration.objects.get_or_create(
            grading_system=SystemConfiguration.GradingSystem.MARKS,
            defaults={
                "auto_unique_ids": True,
                "unique_id_prefix": "IMS",
                "unique_id_padding": 4,
                "default_country": "India",
                "default_currency": "INR",
                "default_time_zone": "Asia/Kolkata",
                "default_language": "en",
            },
        )
        SystemConfiguration.objects.get_or_create(
            grading_system=SystemConfiguration.GradingSystem.GPA,
            defaults={
                "auto_unique_ids": True,
                "unique_id_prefix": "GPA",
                "unique_id_padding": 4,
                "default_country": "India",
                "default_currency": "INR",
                "default_time_zone": "Asia/Kolkata",
                "default_language": "en",
            },
        )

        cat_general, _ = StudentCategory.objects.get_or_create(
            name="General",
            defaults={
                "description": "Regular enrolled students",
                "allows_graduation": True,
            },
        )
        cat_transfer, _ = StudentCategory.objects.get_or_create(
            name="Transfer",
            defaults={
                "description": "Transferred from another institute",
                "allows_graduation": True,
            },
        )

        course_cs, _ = Course.objects.get_or_create(
            code="CS101",
            defaults={
                "name": "Computer Science Basics",
                "description": "Introductory CS course",
                "is_active": True,
            },
        )
        course_math, _ = Course.objects.get_or_create(
            code="MTH101",
            defaults={
                "name": "Mathematics Foundations",
                "description": "Core mathematics course",
                "is_active": True,
            },
        )

        today = timezone.localdate()

        batch_cs_a, _ = Batch.objects.get_or_create(
            course=course_cs,
            code="A",
            defaults={
                "name": "CS Batch A",
                "start_date": today - timedelta(days=120),
                "end_date": today + timedelta(days=240),
                "is_active": True,
            },
        )
        batch_math_a, _ = Batch.objects.get_or_create(
            course=course_math,
            code="A",
            defaults={
                "name": "Math Batch A",
                "start_date": today - timedelta(days=90),
                "end_date": today + timedelta(days=270),
                "is_active": True,
            },
        )

        subj_cs_prog, _ = Subject.objects.get_or_create(
            course=course_cs,
            code="CS-PROG",
            defaults={
                "name": "Programming Fundamentals",
                "is_elective": False,
                "credits": 4.0,
            },
        )
        subj_math_alg, _ = Subject.objects.get_or_create(
            course=course_math,
            code="MTH-ALG",
            defaults={
                "name": "Algebra",
                "is_elective": False,
                "credits": 3.0,
            },
        )

        enr_1, _ = Enrollment.objects.get_or_create(
            student=student_users[0],
            course=course_cs,
            defaults={
                "batch": batch_cs_a,
                "category": cat_general,
                "admission_number": "ADM001",
                "status": Enrollment.Status.ACTIVE,
                "joined_on": today - timedelta(days=100),
                "notes": "Seed enrollment 1",
            },
        )
        enr_2, _ = Enrollment.objects.get_or_create(
            student=student_users[1],
            course=course_math,
            defaults={
                "batch": batch_math_a,
                "category": cat_transfer,
                "admission_number": "ADM002",
                "status": Enrollment.Status.ACTIVE,
                "joined_on": today - timedelta(days=80),
                "notes": "Seed enrollment 2",
            },
        )

        BatchTransfer.objects.get_or_create(
            enrollment=enr_1,
            from_batch=batch_cs_a,
            to_batch=batch_math_a,
            transferred_on=today - timedelta(days=15),
            defaults={
                "reason": "Cross-course workshop",
                "notes": "Temporary movement for activity",
            },
        )
        BatchTransfer.objects.get_or_create(
            enrollment=enr_2,
            from_batch=batch_math_a,
            to_batch=batch_cs_a,
            transferred_on=today - timedelta(days=7),
            defaults={
                "reason": "Lab availability",
                "notes": "Moved for practical sessions",
            },
        )

        exam_mid_cs, _ = Exam.objects.get_or_create(
            course=course_cs,
            batch=batch_cs_a,
            subject=subj_cs_prog,
            title="CS Midterm",
            defaults={
                "exam_type": Exam.ExamType.MARKS,
                "evaluation_method": Exam.EvaluationMethod.STANDARD,
                "group_name": "Midterms",
                "max_marks": 100,
                "passing_marks": 40,
                "scheduled_on": timezone.now() - timedelta(days=3),
                "is_published": True,
            },
        )
        exam_quiz_math, _ = Exam.objects.get_or_create(
            course=course_math,
            batch=batch_math_a,
            subject=subj_math_alg,
            title="Math Quiz 1",
            defaults={
                "exam_type": Exam.ExamType.GRADE,
                "evaluation_method": Exam.EvaluationMethod.GPA,
                "group_name": "Quizzes",
                "max_marks": 20,
                "passing_marks": 8,
                "scheduled_on": timezone.now() - timedelta(days=1),
                "is_published": True,
            },
        )

        Grade.objects.get_or_create(
            exam=exam_mid_cs,
            student=student_users[0],
            defaults={
                "marks_obtained": 78,
                "grade_letter": "A",
                "grade_points": 3.8,
                "remarks": "Good performance",
            },
        )
        Grade.objects.get_or_create(
            exam=exam_quiz_math,
            student=student_users[1],
            defaults={
                "marks_obtained": 16,
                "grade_letter": "A-",
                "grade_points": 3.6,
                "remarks": "Consistent work",
            },
        )

        ExamReport.objects.get_or_create(
            exam=exam_mid_cs,
            course=course_cs,
            batch=batch_cs_a,
            report_type=ExamReport.ReportType.AUTOMATED,
            defaults={
                "generated_by": admin_users[0],
                "summary": "CS midterm summary report",
                "payload": {"average": 74.2, "pass_rate": 0.91},
            },
        )
        ExamReport.objects.get_or_create(
            exam=exam_quiz_math,
            course=course_math,
            batch=batch_math_a,
            report_type=ExamReport.ReportType.QUICK,
            defaults={
                "generated_by": admin_users[1],
                "summary": "Math quiz quick report",
                "payload": {"average": 15.1, "pass_rate": 0.88},
            },
        )

        Attendance.objects.get_or_create(
            student=student_users[0],
            enrollment=enr_1,
            course=course_cs,
            batch=batch_cs_a,
            subject=subj_cs_prog,
            attendance_date=today - timedelta(days=2),
            defaults={
                "status": Attendance.Status.PRESENT,
                "report_type": Attendance.ReportType.DAILY,
                "remarks": "On time",
                "marked_by": admin_users[0],
            },
        )
        Attendance.objects.get_or_create(
            student=student_users[1],
            enrollment=enr_2,
            course=course_math,
            batch=batch_math_a,
            subject=subj_math_alg,
            attendance_date=today - timedelta(days=1),
            defaults={
                "status": Attendance.Status.LATE,
                "report_type": Attendance.ReportType.SUBJECT_WISE,
                "remarks": "Arrived after roll call",
                "marked_by": admin_users[1],
            },
        )

        ReportRequest.objects.get_or_create(
            title="April Exam Summary",
            report_kind=ReportRequest.ReportKind.EXAM,
            defaults={
                "parameters": {"month": "April", "course_codes": ["CS101", "MTH101"]},
            },
        )
        ReportRequest.objects.get_or_create(
            title="Weekly Attendance Digest",
            report_kind=ReportRequest.ReportKind.ATTENDANCE,
            defaults={
                "parameters": {"days": 7, "include_late": True},
            },
        )

        self._print_counts()

    def _upsert_user(self, User, username, email, password, role, first_name, last_name):
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "role": role,
                "first_name": first_name,
                "last_name": last_name,
                "is_active": True,
            },
        )

        changed = False
        if user.email != email:
            user.email = email
            changed = True
        if user.role != role:
            user.role = role
            changed = True
        if user.first_name != first_name:
            user.first_name = first_name
            changed = True
        if user.last_name != last_name:
            user.last_name = last_name
            changed = True
        if not user.is_active:
            user.is_active = True
            changed = True
        if not user.check_password(password):
            user.set_password(password)
            changed = True

        if created or changed:
            user.save()

        return user

    def _print_counts(self):
        User = get_user_model()

        counts = {
            "accounts.User": User.objects.count(),
            "accounts.Configuration": Configuration.objects.count(),
            "accounts.SystemConfiguration": SystemConfiguration.objects.count(),
            "academics.StudentCategory": StudentCategory.objects.count(),
            "academics.Course": Course.objects.count(),
            "academics.Batch": Batch.objects.count(),
            "academics.Subject": Subject.objects.count(),
            "academics.Enrollment": Enrollment.objects.count(),
            "academics.BatchTransfer": BatchTransfer.objects.count(),
            "exams.Exam": Exam.objects.count(),
            "exams.Grade": Grade.objects.count(),
            "exams.ExamReport": ExamReport.objects.count(),
            "attendance.Attendance": Attendance.objects.count(),
            "reports.ReportRequest": ReportRequest.objects.count(),
        }

        for model_name, count in counts.items():
            self.stdout.write(f"{model_name}: {count}")
