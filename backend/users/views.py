from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .permissions import IsAdmin
from .tasks import send_welcome_email
from .serializers import LoginSerializer, UserSerializer

User = get_user_model()


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)


class AuthMeView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    def perform_create(self, serializer):
        user = serializer.save()
        send_welcome_email.delay(user.email)

    @action(detail=True, methods=["post"])
    def set_password(self, request, pk=None):
        user = self.get_object()
        password = request.data.get("password")
        if not password:
            return Response({"detail": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(password)
        user.save()
        return Response({"detail": "Password updated"})