from rest_framework.routers import DefaultRouter

from .views import BatchTransferViewSet, BatchViewSet, CourseViewSet, EnrollmentViewSet, StudentCategoryViewSet, SubjectViewSet

router = DefaultRouter()
router.register(r'student-categories', StudentCategoryViewSet, basename='student-category')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'batches', BatchViewSet, basename='batch')
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')
router.register(r'batch-transfers', BatchTransferViewSet, basename='batch-transfer')

urlpatterns = router.urls