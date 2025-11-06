from __future__ import annotations

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BatchViewSet, MedicineViewSet, SupplierViewSet

router = DefaultRouter()
router.register(r"suppliers", SupplierViewSet, basename="supplier")
router.register(r"medicines", MedicineViewSet, basename="medicine")
router.register(r"batches", BatchViewSet, basename="batch")

urlpatterns = [
    path("", include(router.urls)),
]