from rest_framework.routers import SimpleRouter

from .user.views import UserViewSet
from .company.views import CompanyViewSet, PharmacyViewSet

router = SimpleRouter()
router.register("users", UserViewSet)
router.register("companies", CompanyViewSet)
router.register("pharmacies", PharmacyViewSet)

urlpatterns = router.urls


