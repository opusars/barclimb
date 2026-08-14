from django.core.management.base import BaseCommand

from accounts.services import publish_due_auth_email_deliveries


class Command(BaseCommand):
    help = "Publish due durable authentication-email deliveries without exposing credentials."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=100)

    def handle(self, *args, **options):
        published = publish_due_auth_email_deliveries(limit=options["limit"])
        self.stdout.write(f"Published {published} due authentication email deliveries.")
