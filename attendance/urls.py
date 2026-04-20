from rest_framework.routers import DefaultRouter

from .views import AttendanceViewSet

router = DefaultRouter()
router.register(r'attendance-records', AttendanceViewSet, basename='attendance-record')

urlpatterns = router.urls