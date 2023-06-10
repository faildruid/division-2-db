"""Start Division 2 DB uWSGI server."""
from django_webserver.management.commands.pyuwsgi import Command as uWSGICommand


class Command(uWSGICommand):
    """Help string."""

    help = "Start Division 2 DB uWSGI server."
