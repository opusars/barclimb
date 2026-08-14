from django.urls import path

from .views import (
    CsrfView,
    LoginView,
    LogoutView,
    MeView,
    NativeLoginView,
    NativeLogoutView,
    NativePasswordResetRequestView,
    NativeSignupView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    SessionView,
    SignupView,
    VerificationConfirmView,
    VerificationRequestView,
)

urlpatterns = [
    path("csrf/", CsrfView.as_view(), name="auth-csrf"),
    path("signup/", SignupView.as_view(), name="auth-signup"),
    path("login/", LoginView.as_view(), name="auth-login"),
    path("logout/", LogoutView.as_view(), name="auth-logout"),
    path("session/", SessionView.as_view(), name="auth-session"),
    path("me/", MeView.as_view(), name="auth-me"),
    path(
        "verification/request/", VerificationRequestView.as_view(), name="auth-verification-request"
    ),
    path(
        "verification/confirm/", VerificationConfirmView.as_view(), name="auth-verification-confirm"
    ),
    path(
        "password-reset/request/",
        PasswordResetRequestView.as_view(),
        name="auth-password-reset-request",
    ),
    path(
        "password-reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="auth-password-reset-confirm",
    ),
    path("native/session/", NativeLoginView.as_view(), name="auth-native-login"),
    path("native/signup/", NativeSignupView.as_view(), name="auth-native-signup"),
    path(
        "native/password-reset/request/",
        NativePasswordResetRequestView.as_view(),
        name="auth-native-password-reset-request",
    ),
    path("native/session/revoke/", NativeLogoutView.as_view(), name="auth-native-logout"),
]
