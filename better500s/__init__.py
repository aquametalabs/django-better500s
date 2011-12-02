from os.path import join, dirname
from django.conf import settings

BETTER_500_LOG_DIR = getattr(settings, "BETTER_500_LOG_DIR", join(dirname(__file__), 'logs', 'better_500'))
BETTER_500_FROM_EMAIL = getattr(settings, "BETTER_500_FROM_EMAIL", getattr(settings, "DEFAULT_FROM_EMAIL", None))
BETTER_500_TO_EMAILS = getattr(settings, "BETTER_500_TO_EMAILS", getattr(settings, "ADMINS", None))
BETTER_500_UNCAUGHT_DIR = getattr(settings, "BETTER_500_UNCAUGHT_DIR", "UNCAUGHT")
BETTER_500_AJAX_URL = getattr(settings, "BETTER_500_AJAX_URL", "/500-callback/")
BETTER_500_POST_URL = getattr(settings, "BETTER_500_POST_URL", "/500-saved/")