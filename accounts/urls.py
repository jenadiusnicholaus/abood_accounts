from django.urls import path, include
from rest_framework import routers, serializers, viewsets

from accounts.views import UserViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
