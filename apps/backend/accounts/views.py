from django.contrib.auth import authenticate, login, logout, password_validation
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError, transaction
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .authentication import NativeSessionAuthentication
from .models import EmailActionToken, NativeSession, User
from .rate_limits import client_ip, enforce_rate_limit
from .serializers import (
    CredentialsSerializer,
    EmailSerializer,
    ResetPasswordSerializer,
    SignupSerializer,
    TokenSerializer,
    UserSerializer,
)
from .services import (
    issue_native_session_after_revalidation,
    queue_password_reset,
    queue_verification,
)


class AuthAPIView(APIView):
    """Prevent caches from retaining private account or credential responses."""

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        response["Cache-Control"] = "no-store"
        return response


def _ip(request) -> str:
    return client_ip(request)


def _limit_ip(request, operation: str) -> None:
    enforce_rate_limit(operation, ip=_ip(request))


def _limit_identity(operation: str, identity: str) -> None:
    enforce_rate_limit(operation, ip="identity", identity=identity)


def _authenticate(serializer: CredentialsSerializer):
    return authenticate(
        email=serializer.validated_data["email"],
        password=serializer.validated_data["password"],
    )


class CsrfView(AuthAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"csrf_token": get_token(request)})


@method_decorator(csrf_protect, name="dispatch")
class SignupView(AuthAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        _limit_ip(request, "signup")
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        _limit_identity("signup", serializer.validated_data["email"])
        try:
            with transaction.atomic():
                user = serializer.save()
                queue_verification(user)
        except IntegrityError as error:
            raise ValidationError("Email or username is unavailable.") from error
        login(request, user)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


@method_decorator(csrf_protect, name="dispatch")
class LoginView(AuthAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        _limit_ip(request, "login")
        serializer = CredentialsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        _limit_identity("login", serializer.validated_data["email"])
        user = _authenticate(serializer)
        if user is None:
            return Response(
                {"detail": "Email or password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        login(request, user)
        return Response(UserSerializer(user).data)


@method_decorator(csrf_protect, name="dispatch")
class LogoutView(AuthAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SessionView(AuthAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"authenticated": False, "user": None})
        return Response({"authenticated": True, "user": UserSerializer(request.user).data})


class MeView(AuthAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


@method_decorator(csrf_protect, name="dispatch")
class VerificationRequestView(AuthAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        _limit_ip(request, "verification_resend")
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        _limit_identity("verification_resend", email)
        user = User.objects.filter(email=email, is_email_verified=False).first()
        queue_verification(user)
        return Response({"detail": "If verification is available, an email has been sent."})


@method_decorator(csrf_protect, name="dispatch")
class VerificationConfirmView(AuthAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            token = EmailActionToken.consume(
                serializer.validated_data["token"], EmailActionToken.Purpose.VERIFY_EMAIL
            )
            if token is None:
                raise ValidationError("This verification link is invalid or expired.")
            token.user.is_email_verified = True
            token.user.save(update_fields=["is_email_verified"])
        return Response({"detail": "Email verified."})


@method_decorator(csrf_protect, name="dispatch")
class PasswordResetRequestView(AuthAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        _limit_ip(request, "password_reset")
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        _limit_identity("password_reset", email)
        user = User.objects.filter(email=email, is_active=True).first()
        queue_password_reset(user)
        return Response({"detail": "If the account exists, a reset email has been sent."})


@method_decorator(csrf_protect, name="dispatch")
class PasswordResetConfirmView(AuthAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            token = EmailActionToken.consume(
                serializer.validated_data["token"], EmailActionToken.Purpose.RESET_PASSWORD
            )
            if token is None:
                raise ValidationError("This reset link is invalid or expired.")
            try:
                password_validation.validate_password(
                    serializer.validated_data["new_password"], token.user
                )
            except DjangoValidationError as error:
                raise ValidationError({"new_password": list(error.messages)}) from error
            token.user.set_password(serializer.validated_data["new_password"])
            token.user.auth_generation += 1
            token.user.save(update_fields=["password", "auth_generation"])
            NativeSession.objects.filter(user=token.user, revoked_at__isnull=True).update(
                revoked_at=token.used_at
            )
        return Response({"detail": "Password reset. Sign in with your new password."})


class NativeLoginView(AuthAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        _limit_ip(request, "native_session")
        serializer = CredentialsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        _limit_identity("native_session", serializer.validated_data["email"])
        user = _authenticate(serializer)
        if user is None:
            return Response(
                {"detail": "Email or password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        issued = issue_native_session_after_revalidation(
            user, serializer.validated_data["password"]
        )
        if issued is None:
            return Response(
                {"detail": "Email or password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        session, raw, user = issued
        return Response(
            {
                "token": raw,
                "expires_at": session.expires_at,
                "user": UserSerializer(user).data,
            }
        )


class NativeSignupView(AuthAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        _limit_ip(request, "signup")
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        _limit_identity("signup", serializer.validated_data["email"])
        try:
            with transaction.atomic():
                user = serializer.save()
                session, raw = NativeSession.issue(user)
                queue_verification(user)
        except IntegrityError as error:
            raise ValidationError("Email or username is unavailable.") from error
        return Response(
            {"token": raw, "expires_at": session.expires_at, "user": UserSerializer(user).data},
            status=status.HTTP_201_CREATED,
        )


class NativePasswordResetRequestView(AuthAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        _limit_ip(request, "password_reset")
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        _limit_identity("password_reset", email)
        user = User.objects.filter(email=email, is_active=True).first()
        queue_password_reset(user)
        return Response({"detail": "If the account exists, a reset email has been sent."})


class NativeLogoutView(AuthAPIView):
    authentication_classes = [NativeSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.revoke()
        return Response(status=status.HTTP_204_NO_CONTENT)
