from rest_framework.routers import DefaultRouter

from .views import ReportRequestViewSet

router = DefaultRouter()
router.register(r'requested-reports', ReportRequestViewSet, basename='report-request')

urlpatterns = router.urls