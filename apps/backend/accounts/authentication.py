from django.utils import timezone
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import NativeSession, hash_secret


class NativeSessionAuthentication(BaseAuthentication):
    keyword = "Bearer"

    def authenticate(self, request):
        header = request.headers.get("Authorization", "")
        if not header:
            return None
        parts = header.split()
        if len(parts) != 2 or parts[0].lower() != self.keyword.lower():
            raise AuthenticationFailed("Invalid native session credential")
        try:
            session = NativeSession.objects.select_related("user").get(
                token_hash=hash_secret(parts[1])
            )
        except NativeSession.DoesNotExist as error:
            raise AuthenticationFailed("Invalid or expired native session") from error
        if not session.is_valid:
            raise AuthenticationFailed("Invalid or expired native session")
        session.last_used_at = timezone.now()
        session.save(update_fields=["last_used_at"])
        return session.user, session

    def authenticate_header(self, request):
        return self.keyword
