from django.urls import path, include
from rest_framework import routers, serializers, viewsets

from accounts.views import AccountViewSet

router = routers.DefaultRouter()
router.register(r"accounts-vset", AccountViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
