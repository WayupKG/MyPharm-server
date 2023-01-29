from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('token/', jwt_views.TokenObtainPairView.as_view(), name="token"),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path('token/verify/', jwt_views.TokenVerifyView.as_view(), name="token_verify"),
    path('token/blacklist/', jwt_views.TokenBlacklistView.as_view(), name="token_blacklist"),
]
