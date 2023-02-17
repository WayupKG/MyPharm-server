from rest_framework.routers import SimpleRouter

from .user.views import UserViewSet
from .company.views import CompanyViewSet, PharmacyViewSet
from .medicine.views import CategoryViewSet, MedicineViewSet

router = SimpleRouter()
router.register("users", UserViewSet)
router.register("companies", CompanyViewSet)
router.register("pharmacies", PharmacyViewSet)
router.register("categories", CategoryViewSet)
router.register("medicines", MedicineViewSet)

urlpatterns = router.urls


