from django.urls import path, include

urlpatterns = [
    path('users/', include('api.version_1.user.urls'))
]
