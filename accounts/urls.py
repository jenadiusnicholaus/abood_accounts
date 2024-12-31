from django.urls import path, include
from rest_framework import routers, serializers, viewsets

from accounts.views import AccountCRDRViewSet, AccountDRCRViewSet, CompanyAccountViewSet

router = routers.DefaultRouter()
router.register(
    r"accounts-sales-cr-dr-vset",
    AccountCRDRViewSet,
    basename="accounts-sales-cr-dr-vset",
)
router.register(
    r"accounts-sales-dr-cr-vset",
    AccountDRCRViewSet,
    basename="accounts-sales-dr-cr-vset",
)
router.register(
    r"company-accounts-vset",
    CompanyAccountViewSet,
    basename="company-accounts-vset",
)

urlpatterns = [
    path("", include(router.urls)),
]
