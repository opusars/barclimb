import logging
from urllib.parse import parse_qs, urlparse

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

logger = logging.getLogger("barclimb.staging_email")


class StagingAuthEmailSink(BaseEmailBackend):
    """Validate auth delivery shape without delivering or logging private data."""

    def send_messages(self, email_messages):
        count = 0
        expected = urlparse(settings.PUBLIC_BASE_URL)
        for message in email_messages or ():
            links = [part for part in message.body.split() if part.startswith("https://")]
            if len(links) != 1:
                raise ValueError("staging auth email must contain exactly one HTTPS action link")
            action = urlparse(links[0])
            if (action.scheme, action.netloc) != (expected.scheme, expected.netloc):
                raise ValueError("staging auth email must use PUBLIC_BASE_URL")
            if action.path not in {"/verify-email", "/reset-password"} or action.query:
                raise ValueError("staging auth email has an invalid action route")
            fragment = parse_qs(action.fragment, keep_blank_values=True)
            if (
                set(fragment) != {"token"}
                or len(fragment["token"]) != 1
                or not fragment["token"][0]
            ):
                raise ValueError("staging auth email must carry one fragment token")
            count += 1
            logger.info("staging auth email accepted action=%s", action.path)
        return count
