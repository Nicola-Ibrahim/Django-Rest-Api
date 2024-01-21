from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import (
    CompanyViewSet,
    LocationGroupViewSet,
    LocationTagViewSet,
    LocationViewSet,
    ZoneTypeViewSet,
    ZoneViewSet,
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()


router.register(r"zone-type", ZoneTypeViewSet)
router.register(r"zone", ZoneViewSet)
router.register(r"location-group", LocationGroupViewSet)
router.register(r"location-tag", LocationTagViewSet)
router.register(r"location", LocationViewSet)
router.register(r"company", CompanyViewSet)


app_name = "api"
urlpatterns = router.urls
