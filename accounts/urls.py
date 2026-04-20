from rest_framework.routers import DefaultRouter

from .views import ConfigurationViewSet, SystemConfigurationViewSet, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'configurations', ConfigurationViewSet, basename='configuration')
router.register(r'system-configurations', SystemConfigurationViewSet, basename='system-configuration')

urlpatterns = router.urls