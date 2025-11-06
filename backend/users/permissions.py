from __future__ import annotations

from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import User


class IsAdmin(BasePermission):
    def has_permission(self, request, view) -> bool:
        return bool(request.user and request.user.is_authenticated and request.user.role == User.Role.ADMIN)


class IsAdminOrPharmacist(BasePermission):
    def has_permission(self, request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return request.user.role in {User.Role.ADMIN, User.Role.PHARMACIST}