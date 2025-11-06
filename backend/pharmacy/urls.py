from __future__ import annotations

from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from alerts.urls import router as alerts_router
from inventory.urls import router as inventory_router
from sales.urls import router as sales_router
from rest_framework_simplejwt.views import TokenRefreshView
from users.urls import router as users_router
from users.views import AuthMeView, LoginView, LogoutView

router = routers.DefaultRouter()
router.registry.extend(inventory_router.registry)
router.registry.extend(sales_router.registry)
router.registry.extend(alerts_router.registry)
router.registry.extend(users_router.registry)

api_urlpatterns = [
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/me/", AuthMeView.as_view(), name="auth-me"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("inventory/", include("inventory.urls")),
    path("sales/", include("sales.urls")),
    path("alerts/", include("alerts.urls")),
    path("reports/", include("reports.urls")),
    path("", include("users.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include((api_urlpatterns, "api"))),
    path("api/", include(router.urls)),
]