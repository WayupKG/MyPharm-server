from rest_framework.routers import SimpleRouter

from .user.views import UserViewSet

router = SimpleRouter()
router.register("users", UserViewSet)

urlpatterns = router.urls


