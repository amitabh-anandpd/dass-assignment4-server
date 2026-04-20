from rest_framework.routers import DefaultRouter

from .views import ExamReportViewSet, ExamViewSet, GradeViewSet

router = DefaultRouter()
router.register(r'exams', ExamViewSet, basename='exam')
router.register(r'grades', GradeViewSet, basename='grade')
router.register(r'exam-reports', ExamReportViewSet, basename='exam-report')

urlpatterns = router.urls